import logging
import os
import re
import shutil
from dataclasses import dataclass, field
from typing import List, Union, Tuple

import markdown as md
import treefiles as tf
from htmlmin import minify
from jinja2 import Environment, select_autoescape, FileSystemLoader


@dataclass
class BaseBlock:
    html: str = ""
    assets: List[str] = field(default_factory=list)


class BlockHolder:
    def __init__(self, *blocks: Union[List, Tuple, BaseBlock, "BlockHolder"], **kw):
        self.blocks: List[Union[BaseBlock, BlockHolder]] = list(
            tf.get_iterable(tf.none(blocks, []))
        )
        self.kw = kw

    def markdown(self, txt, *classes):
        x = md.markdown(txt, extensions=["fenced_code"])
        cls = ' '.join(classes)
        self.blocks.append(
            BlockHolder(BaseBlock(x)).wrap(f'<div class="{cls}">')
        )
        return self

    def vspace(self, val):
        self.blocks.append(BaseBlock(f'<div style="height: {val}px"></div>'))
        return self

    @property
    def html(self):
        return "".join([x.html for x in self.blocks])

    @property
    def assets(self):
        aa = []
        for x in self.blocks:
            aa.extend(x.assets)
        return aa

    def add_asset(self, ct):
        self.blocks.append(BaseBlock("", [ct]))

    def wrap(self, bfr, aft=None):
        """
        Add a block at the beginning and at the end of this holder
        :param bfr: html to add before
        :param aft: html to close (tag is extracted from bfr if None)
        """
        self.blocks.insert(0, BaseBlock(bfr))
        if aft is None:
            m = re.search(r"^<(\w+) ", bfr)
            aft = rf"</{m.group(1)}>"
        self.blocks.append(BaseBlock(aft))
        return self

    def row(self, *cols: "BlockHolder"):
        """
        Add html elements with bootstrap grid system
        https://getbootstrap.com/docs/4.0/layout/grid/
        """
        cols = BlockHolder(*cols)
        for x in cols.blocks:
            width = x.kw.get("width")
            col_w = f"col-{width}" if width else x.kw.get("col", "col")
            x.wrap(f'<div class="{col_w}">')
        cols.wrap(f'<div class="row">')
        self.blocks.append(cols)
        return self

    def nav(self, *onglets: "BlockHolder"):
        """
        Add onglets html elements and a navbar
        https://getbootstrap.com/docs/4.0/components/navs/
        """
        nav = BlockHolder()
        elems = BlockHolder(*onglets)
        for x in elems.blocks:
            idx = x.kw["title"].lower().replace(" ", "_")
            idx += tf.get_string()
            ac = "active" if x.kw.get("active") else ""
            x.wrap(f'<div id="{idx}" class="tab-pane fade show {ac}">')
            x_link = BaseBlock(
                f'<a class="nav-link {ac}" aria-current="page" data-toggle="tab" href="#{idx}">{x.kw["title"]}</a>'
            )
            nav.blocks.append(BlockHolder(x_link).wrap('<li class="nav-item active">'))
        elems.wrap('<div class="tab-content">')
        nav.wrap('<ul class="nav nav-tabs">')
        self.blocks.append(nav)
        self.blocks.append(elems)
        return self

    def dataframe(self, df, *classes: Union[str, List[str]], **kw):
        """
        Add a dataframe wrapped in bootstrap table
        https://getbootstrap.com/docs/4.0/content/tables/
        https://getbootstrap.com/docs/4.1/utilities/sizing/
        :param df: input dataframe
        :param classes: Bootstrap classes ex: w-25 text-center
        """
        kw = {"border": 0, "index": False, **kw, "escape": False}
        html = df.to_html(classes=["table", *tf.get_iterable(classes)], **kw)
        html = html.replace(' style="text-align: right;"', "")
        html = html.replace("<th>", "<th scope='col'>")
        self.blocks.append(BaseBlock(html))
        return self

    def lines(self, **kw):
        from htmlit2.plotly_utils import make_plotly_line

        html = make_plotly_line(**kw)
        self.blocks.append(BaseBlock(html))
        return self

    def figure(self, fname, title: str = None):
        if fname.endswith(".mp4"):
            fig = BlockHolder.new(f'<source src="{fname}" type="video/mp4">')
            fig.wrap('<video width="480" height="320" controls autoplay loop>')
        else:
            fig = BlockHolder.new(f'<img src="{fname}" class="img-fluid">')
            fig.wrap(f'<a href="{fname}">')

        fig.add_asset(fname)
        if title:
            caption = BlockHolder.new(title).wrap(
                '<figcaption class="figure-caption text-center">'
            )
            fig.blocks.append(caption)
        self.blocks.append(fig.wrap('<figure class="figure">'))
        return self

    @classmethod
    def new(cls, *ct):
        return cls(*[BaseBlock(x) for x in ct])

    def add_html(self, x):
        self.blocks.append(BaseBlock(x))


class Generator:
    def __init__(self, holder: BlockHolder, title: str = None):
        self.title = title
        self.holder = holder
        self.env = Environment(
            loader=FileSystemLoader(tf.f(__file__) / "templates"),
            autoescape=select_autoescape(),
        )

    def render(
        self,
        out_dir: tf.TS,
        save_zip: bool = False,
        clean=True,
    ):
        """
        Fill the template with the holder's content
        :param out_dir: output directory (where the output html is written)
        :param save_zip: if a zip file should be created
        :param clean: delete out_dir content before export
        """
        out_dir = tf.Tree(out_dir).dump(clean).abs()
        template = self.env.get_template("index.html")
        html = template.render(
            enumerate=enumerate,
            python_dyn=self.holder.html,
            title=tf.none(self.title, "htmlit2 report"),
        )

        # Deal with assets
        for x in self.holder.assets:
            a, b = os.path.splitext(tf.basename(x))
            nname = f"{a}_{tf.get_string()}{b}"
            tf.copyFile(x, out_dir / nname)
            html = html.replace(x, nname)

        html = minify(html.replace("\u2013", "-"), remove_empty_space=True)
        fname = out_dir / "index.html"
        tf.dump_str(fname, html)
        log.info(f"HTML report wrote to file://{fname}")

        if save_zip:
            shutil.make_archive(out_dir, "zip", out_dir.parent.abs(), out_dir.basename)
            tf.logf(out_dir + ".zip")


log = logging.getLogger(__name__)
logging.getLogger("MARKDOWN").setLevel(logging.INFO)
