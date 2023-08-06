import logging

import lorem
import treefiles as tf

from htmlit2.block import BlockHolder, Generator


def main():
    out_dir = tf.f(__file__) / "report"

    main_ = BlockHolder()

    main_.markdown("# Hello")
    html = BlockHolder(title="Main 1", active=True)
    html.markdown("# Hellddo")
    html.markdown(lorem.paragraph())

    col1 = BlockHolder(width=4)
    col1.markdown("# Column 1")
    col2 = BlockHolder().markdown("# Column 2").markdown(lorem.paragraph())
    onglet1 = BlockHolder(title="Onglet 1", active=True)
    onglet1.markdown("# Title onglet 1")
    onglet2 = BlockHolder(title="Onglet 2")
    onglet2.markdown("# Title onglet 2")

    col1.nav(onglet1, onglet2)
    html.row(col1, col2)
    html2 = BlockHolder(title="Main 2")

    main_.nav(html, html2)
    main_.markdown("the end...")

    gen = Generator(main_, title="results")
    gen.render(out_dir)


log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger()

    main()
