import logging

import pandas as pd
import treefiles as tf

from htmlit2.block import BlockHolder, Generator


def main():
    out_dir = tf.f(__file__) / "report"
    fig_fname = tf.f(__file__) / "fig.png"
    df = pd.DataFrame({"a": range(3), "b": range(10, 13)})
    with tf.APlot(fname=fig_fname, show=False) as (fig, ax):
        ax.plot(df["a"], df["b"])
        ax.set_xlabel("Test")

    main_block = BlockHolder()

    main_block.markdown("## DataFrame")
    main_block.dataframe(df, "w-25", "text-center", "mt-4")

    main_block.markdown("## Plot")
    main_block.lines(x=df["a"], y=df["b"], x_label="Test")

    main_block.markdown("## Image")
    main_block.figure(fig_fname, "My figure")

    gen = Generator(main_block, title="results")
    gen.render(out_dir)


log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger()

    main()
