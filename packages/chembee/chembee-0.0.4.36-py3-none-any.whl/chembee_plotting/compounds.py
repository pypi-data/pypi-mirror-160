from rdkit.Chem import Draw


def plot_compound_list(mols, file_nam):
    """
    The plot_compound_list function takes a list of RDKit molecules and plots them in a grid.
    The function takes two arguments:
        mols - A list of RDKit molecules to plot.
        file_name - The name of the image file to save the plot as, including the extension (.png, .svg, etc.).

    :param mols: Used to specify the list of molecules to be drawn.
    :param file_nam: Used to name the image file.
    :return: A plot of the molecules in a list.

    :doc-author: Julian M. Kleber
    """

    drawOptions = Draw.rdMolDraw2D.MolDrawOptions()
    drawOptions.prepareMolsBeforeDrawing = False
    img = Draw.MolsToGridImage(
        mols,
        molsPerRow=5,
        subImgSize=(200, 200),
        legends=[
            x.GetProp("ReadyBiodegradability") + "    " + x.GetProp("Dataset")
            for x in mols
        ],
    )
    img.save(file_name)
    raise NotImplementedError("Not yet tested")
