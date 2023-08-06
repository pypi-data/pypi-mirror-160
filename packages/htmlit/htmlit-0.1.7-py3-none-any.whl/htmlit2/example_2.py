import logging

import lorem
import pandas as pd
import treefiles as tf

from htmlit2.block import BlockHolder, Generator


def main():
    out_dir = tf.f(__file__) / "report"

    fig_fname = tf.f(__file__) / "fig.png"
    df = pd.DataFrame({"a": range(3), "b": range(10, 13)})
    with tf.APlot(fname=fig_fname, show=False) as (fig, ax):
        ax.plot(df["a"], df["b"], label="test")

    main_block = BlockHolder()

    main_block.markdown("# Hello")
    main_block.markdown(lorem.paragraph())

    ong1 = BlockHolder(title="Resultats", active=True)
    ong1.vspace(20)
    ong1.markdown("### Results")
    ong1.markdown(lorem.paragraph())
    ong1.lines(x=df["a"], y=df["b"], x_label="Test")

    ong2 = BlockHolder(title="Infos").vspace(20)
    ong2.markdown("### Informations")

    r1 = (
        BlockHolder()
        .markdown(lorem.paragraph())
        .dataframe(df, "w-50", "text-center", "mt-4")
    )
    r2 = BlockHolder().figure(fig_fname, "My figure")
    ong2.row(r1, r2)

    ong3 = BlockHolder(title="Nested").vspace(20)
    ong11 = BlockHolder(title="Nested 1").vspace(20).markdown(lorem.paragraph())
    ong12 = (
        BlockHolder(title="Nested 2", active=True)
        .vspace(20)
        .markdown(lorem.paragraph())
    )
    ong3.nav(ong11, ong12)

    ong4 = BlockHolder(title="Code").vspace(20)
    ong4.markdown(f"``` python\n{tf.load_str(__file__)}\n```")

    main_block.vspace(50)
    main_block.nav(ong1, ong2, ong3, ong4)
    main_block.vspace(400)

    gen = Generator(main_block, title="results")
    gen.render(out_dir)


log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger()

    main()
