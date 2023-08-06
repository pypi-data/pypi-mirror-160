import logging
import os.path
import shutil
from collections import defaultdict
from typing import List

import markdown as md
import pandas as pd
import treefiles as tf
from htmlmin import minify
from jinja2 import Environment, PackageLoader, select_autoescape


class BaseBlock:
    def __init__(self, content, assets=None, **kw):
        self.content = content
        self.assets = tf.none(assets, [])
        self.kw = kw
        self._html = None
        self.html = self.content
        self.init()

    def init(self):
        pass

    @property
    def html(self) -> str:
        h = ""
        if "mt" in self.kw:
            h += f"""<div style='height: {self.kw["mt"]}px'></div>"""
        h += tf.none(self._html, "")
        if "mb" in self.kw:
            h += f"""<div style='height: {self.kw["mb"]}px'></div>"""
        return h

    @html.setter
    def html(self, value):
        raise NotImplementedError

    def copy_assets(self, out_dir):
        for x in self.assets:
            a, b = os.path.splitext(tf.basename(x))
            nname = f"{a}_{tf.get_string()}{b}"
            tf.copyFile(x, out_dir / nname)
            self.html = self.html.replace(x, nname)


class ImgBlock(BaseBlock):
    def init(self):
        self.assets.append(self.content)

    @BaseBlock.html.setter
    def html(self, value: str):
        self._html = IMG.format(src=value)


class FigBlock(BaseBlock):
    def init(self):
        self.assets.append(self.content)

    @BaseBlock.html.setter
    def html(self, src: str):
        cap = self.kw.get("caption")
        txt = f'<figure class="figure">'
        txt += f'<a href="{src}"><img src="{src}" class="img-fluid"></a>'
        if cap:
            txt += f'<figcaption class="figure-caption text-center">{cap}</figcaption>'
        txt += "</figure>"
        self._html = txt


class VideoBlock(BaseBlock):
    def init(self):
        self.assets.append(self.content)

    @BaseBlock.html.setter
    def html(self, value: str):
        self._html = VID.format(src=value)


class TexBlock(BaseBlock):
    @BaseBlock.html.setter
    def html(self, value: str):
        self._html = f"$${value}$$"


class MdBlock(BaseBlock):
    @BaseBlock.html.setter
    def html(self, value: str):
        self._html = md.markdown(value, extensions=["fenced_code"])


class DfBlock(BaseBlock):
    @BaseBlock.html.setter
    def html(self, value: pd.DataFrame):
        self._html = (
            value.to_html(classes=["table"], border=0, index=False, escape=False)
            .replace(' style="text-align: right;"', "")
            .replace("<th>", "<th scope='col'>")
        )


class RowBlock(BaseBlock):
    @BaseBlock.html.setter
    def html(self, value: str):
        self._html = value


class RawBlock(BaseBlock):
    @BaseBlock.html.setter
    def html(self, value: str):
        self._html = value


class HtmlGenerator:
    def __init__(self, new_env=True):
        self.python_dyn: List[BaseBlock] = []

        if new_env:
            self.env = Environment(
                loader=PackageLoader("htmlit.HtmlGenerator"),
                autoescape=select_autoescape(),
            )

        self.nav_items = []

    def get_include(self, out_dir, clean: bool = True):
        out_dir = tf.Tree(out_dir).dump(clean=clean)
        for x in self.python_dyn:
            x.copy_assets(out_dir)

        space = lambda x: f"<div style='height: {x}px'></div>"
        python_dyn = space(10).join([x.html for x in self.python_dyn])
        python_dyn = f"{python_dyn}{space(400)}"
        return python_dyn

    def render(self, out_dir: tf.T, save_zip: bool = False, clean=True):
        out_dir = tf.Str(out_dir)

        # Main page content
        python_dyn = self.get_include(out_dir, clean=clean)

        # Add nav bar if onglets
        if len(self.nav_items) > 0:
            ss = '<ul class="nav nav-tabs">\n'
            for i, x in enumerate(self.nav_items):
                ss += (
                    NAV.format(
                        active="active" if i == 0 else "",
                        idx=x.lower().replace(" ", "_"),
                        name=x,
                    )
                    + "\n"
                )
            ss += "</ul>"
            python_dyn = ss + '<div class="tab-content">\n' + python_dyn + "</div>"

        template = self.env.get_template("index.html")
        aa = template.render(
            enumerate=enumerate,
            python_dyn=python_dyn,
        )
        aa = aa.replace("\u2013", "-")

        aa = minify(aa, remove_empty_space=True)

        fname = out_dir / "index.html"
        tf.dump_str(fname, aa)
        log.info(f"HTML report wrote to file://{fname}")

        if save_zip:
            shutil.make_archive(out_dir, "zip", out_dir.parent.abs(), out_dir.basename)
            tf.logf(out_dir + ".zip")

    def vspace(self, val):
        self.markdown(mt=val)

    def code(self, val, lang="python", **kw):
        self.markdown(MDCode.format(code=val, lang=lang), **kw)

    def markdown(self, s="", **kw):
        self.python_dyn.append(MdBlock(s, **kw))

    def latex(self, s):
        self.python_dyn.append(TexBlock(s))

    def image(self, src: str):
        self.python_dyn.append(ImgBlock(src))

    def figure(self, src: str, caption: str = None):
        self.python_dyn.append(FigBlock(src, caption=caption))

    def dataframe(self, df: pd.DataFrame):
        self.python_dyn.append(DfBlock(df))

    def video(self, src: str):
        self.python_dyn.append(VideoBlock(src))

    @property
    def row(self):
        class Row(HtmlGenerator):
            def __init__(s):
                super().__init__(new_env=False)
                s.col_keys = []

            def __enter__(s):
                return s

            def __call__(s, idx, key="col"):
                s.col_keys.append((idx, key))
                return s

            def __exit__(s, exc_type, exc_val, exc_tb):
                txt = "<div class='row'>\n"
                blocks = defaultdict(list)
                assets = []
                for ck, block in zip(s.col_keys, s.python_dyn):
                    blocks[ck[0]].append((block, ck[1]))
                    assets.extend(block.assets)
                for k, v in blocks.items():
                    txt += f"<div class='{v[0][1]}'>\n"
                    for bv, _ in v:
                        txt += bv.html + "\n"
                    txt += "</div>\n"
                txt += "</div>\n"
                self.python_dyn.append(RowBlock(txt, assets=assets))

        return Row()

    @property
    def onglet(self):
        class Onglet:
            def __init__(s, name):
                s.name = name

            def __enter__(s):
                s.j = len(self.python_dyn)
                return s

            def __exit__(s, exc_type, exc_val, exc_tb):
                idx = s.name.lower().replace(" ", "_")
                ac = "active" if len(self.nav_items) == 0 else ""
                txt = f'<div id="{idx}" class="tab-pane fade show {ac}">\n'
                # txt += f'<h3 class="mt-4 mb-3">{s.name}</h3>\n'
                self.python_dyn.insert(s.j, RawBlock(txt))
                self.python_dyn.append(RawBlock("</div>\n"))
                self.nav_items.append(s.name)

        return Onglet


IMG = """
<div>
    <a href="{src}">
        <img src="{src}" class="img-fluid">
    </a>
</div>
""".strip()
VID = """
<div>
    <video width="480" height="320" controls="controls">
        <source src="{src}" type="video/mp4">
    </video>
</div>
""".strip()
NAV = """
<li class="nav-item active">
    <a class="nav-link {active}" aria-current="page" data-toggle="tab" href="#{idx}">{name}</a>
</li>
""".strip()
MDCode = """
```{lang}
{code}
```
""".strip()


log = logging.getLogger(__name__)
logging.getLogger("MARKDOWN").setLevel(logging.INFO)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger()

    gen = HtmlGenerator()
    gen.render(tf.f(__file__) / "test.html")
