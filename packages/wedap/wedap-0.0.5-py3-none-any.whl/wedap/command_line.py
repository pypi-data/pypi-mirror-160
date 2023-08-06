"""
Functions for handling command-line input using argparse module.

TODO: add option to split pdist and plot once the pdist to txt feature is done
      so the pdist txt file could be: X_column, Y_column, Z_matrix_columns.
      This would be something like pdist.dap default and option to check and 
      read in a wedap or westpa pdist file for pdist function.
"""

import argparse
from inspect import trace
import os
import sys

from pip import main

# import and use gooey conditionally
# adapted from https://github.com/chriskiehl/Gooey/issues/296
try:
    import gooey
    #from gooey import Gooey
    #from gooey import GooeyParser
except ImportError:
    gooey = None

def flex_add_argument(f):
    '''Make the add_argument accept (and ignore) the widget option.'''

    def f_decorated(*args, **kwargs):
        kwargs.pop('widget', None)
        return f(*args, **kwargs)

    return f_decorated

# Monkey-patching a private class…
argparse._ActionsContainer.add_argument = \
    flex_add_argument(argparse.ArgumentParser.add_argument)

# Do not run GUI if it is not available or if command-line arguments are given.
if gooey is None or len(sys.argv) > 1:
    ArgumentParser = argparse.ArgumentParser

    def gui_decorator(f):
        return f
else:
    ArgumentParser = gooey.GooeyParser
    gui_decorator = gooey.Gooey(
        program_name='wedap',
        #navigation='TABBED',
        #advanced=True,
        suppress_gooey_flag=True,
        optional_cols=4, 
        default_size=(1000, 600),
        #tabbed_groups=True,
    )

# TODO: make tabs
# then push new pip version
@gui_decorator
def create_cmd_arguments(): 
    """
    Use the `argparse` module to make the optional and required command-line
    arguments for the `wedap`. 

    Parameters 
    ----------

    Returns
    -------
    argparse.ArgumentParser: 
        An ArgumentParser that is used to retrieve command line arguments. 
    """
    wedap_desc = """Weighted Ensemble data analysis and plotting (wedap): \n
                 Given an input west.h5 file from a successful WESTPA simulation, prepare probability distributions and plots."""

    # create argument parser (gooey based if available)
    if gooey is None:
        parser = argparse.ArgumentParser(description = wedap_desc)
    else:
        parser = gooey.GooeyParser(description = wedap_desc)

    ##########################################################
    ############### REQUIRED ARGUMENTS #######################
    ##########################################################

    # create new group for required args 
#     required_args = parser.add_argument_group("Required Arguments") 

#     # create file flag  
#     required_args.add_argument("-h5", "--h5file", required = True, help = "The \
#         WESTPA west.h5 output file that will be analyzed.", action = "store", 
#         dest = "h5", type=str) 

    # specify the main group of args needed and shown on initial page
    # note that these are positional arguments to parser
    # so like $ plothist average
    # good for different tools, maybe good for movie
    #main = parser.add_subparsers(help="Main Arguments", dest="Main")
    # sub_main = main.add_parser('option1')
    # sub_main.add_argument("test")
    # sub_main2 = main.add_parser('option2')
    # sub_main2.add_argument("test")

    # test out gooey specific widgets
    required = parser.add_argument_group("Required Arguments")
    required.add_argument("-h5", "--h5file", #required=True, nargs="?",
        default="west.h5", action="store", dest="h5", type=str,
        help="The WESTPA west.h5 output file that will be analyzed. "
             "Default 'west.h5'.", 
        widget="FileChooser")

    ###########################################################
    ############### OPTIONAL ARGUMENTS ########################
    ###########################################################
    # nargs = '?' "One argument will be consumed from the command line if possible, 
        # and produced as a single item. If no command-line argument is present, 
        # the value from default will be produced."

    # TODO: I should add histrange_x and histrange_y

    main = parser.add_argument_group("Main Arguments")
    optional = parser.add_argument_group("Optional Extra Arguments")

    main.add_argument("-dt", "--data-type", default="evolution", nargs="?",
                        dest="data_type", choices=("evolution", "average", "instant"),
                        help="Type of pdist dataset to generate, options are"
                             "'evolution' (1 dataset);" 
                             "'average' or 'instance' (1 or 2 or 3 datasets)",
                        type=str) 
    main.add_argument("-pm", "--plot-mode", default="hist2d", nargs="?",
                        dest="plot_mode", choices=("hist2d", "contour", "bar", 
                                                   "line", "scatter3d"),
                        help="The type of plot desired, current options for: "
                             "1D: 'line', 2D: 'hist2d', 'contour', 3D: 'scatter3d'",
                        type=str)
    # TODO: could make choices tuple with the available aux values from the h5 file
    main.add_argument("-X", "--Xname", default="pcoord", nargs="?",
                        dest="Xname", #choices=aux, TODO
                        help="Target data name for x axis. Default 'pcoord', "
                        "can also be any aux dataset name in your h5 file.",
                        type=str)
    main.add_argument("-Y", "--Yname", default=None, nargs="?",
                        dest="Yname", #choices=aux, TODO
                        help="Target data name for y axis. Default 'None', "
                        "can be 'pcoord' or any aux dataset name in your h5 file.",
                        type=str)
    main.add_argument("-Z", "--Zname", default=None, nargs="?",
                        dest="Zname", #choices=aux, TODO
                        help="Target data name for z axis. Must use 'scatter3d' "
                        "for 'plot_mode'. Can be 'pcoord' or any aux dataset name "
                        "in your h5 file.",
                        type=str)
    main.add_argument("-Xi", "--Xindex", default=0, nargs="?", type=int,
                        dest="Xindex", help="Index in third dimension for >2D datasets.")
    main.add_argument("-Yi", "--Yindex", default=0, nargs="?", type=int,
                        dest="Yindex", help="Index in third dimension for >2D datasets.")
    main.add_argument("-Zi", "--Zindex", default=0, nargs="?", type=int,
                        dest="Zindex", help="Index in third dimension for >2D datasets.")
    main.add_argument("-o", "--output", default=None,
                        dest="output_path",
                        help="The filename to which the plot will be saved. "
                             "Various image formats are available. You " 
                             "may choose one by specifying an extension. "
                             "\nLeave this empty if you don't want to save "
                             "the plot to a serperate file",
                        type=str)
    # begin optional arg group
    optional.add_argument("--first-iter", default=1, nargs="?",
                        dest="first_iter",
                        help="Plot data starting at iteration FIRST_ITER."
                             "By default, plot data starting at the first"
                             "iteration in the specified west.h5 file.",
                        type=int)
    optional.add_argument("--last-iter", default=None, nargs="?",
                        dest="last_iter",
                        help="Plot data up to and including iteration LAST_ITER."
                             "By default, plot data up to and including the last "
                             "iteration in the specified H5 file.",
                        type=int)
    optional.add_argument("--bins", default=100, nargs="?",
                        dest="bins",
                        help="Use BINS number of bins for histogramming "
                             "Divide the range between the minimum and maximum "
                             "observed values into this many bins",
                        type=int)
    optional.add_argument("--pmin", default=0, nargs="?",
                        dest="p_min",
                        help="The minimum probability value limit."
                             "This determines the cbar limits and contour levels.",
                        type=int)
    optional.add_argument("--pmax", default=None, nargs="?",
                        dest="p_max",
                        help="The maximum probability limit value."
                             "This determines the cbar limits and contour levels.",
                        type=int)
    optional.add_argument("--punits", default="kT", nargs="?",
                        dest="p_units", choices=("kT", "kcal"),
                        help="Can be 'kT' (default) or 'kcal'."
                             "kT = -lnP, kcal/mol = -RT(lnP), "
                             "where RT=0.5922 at T(298K).",
                        type=str)
    optional.add_argument("-T", "--temp", default=298, nargs="?",
                        dest="T", help="Used with kcal/mol 'p_unit'.",
                        type=int)
    # TODO: is there a better way to do this?
    # TODO: not sure if this works properly
    #optional.add_argument("--weighted", default=True, action="store_true",
    #                      help="Use weights from WE.")
    optional.add_argument("-nw", "--not_weighted",
                          help="Include this to not use WE weights.",
                          dest="not_weighted", action="store_true")
    # optional.add_argument("--weighted", default=True, 
    #                       action=argparse.BooleanOptionalAction)

    optional.add_argument("--style", default="default", nargs="?",
                        dest="style",
                        help="mpl style, can use default, None, or custom. "
                             "Edit the wedap/styles/default.mplstyle file to "
                             "change default wedap plotting style options.",
                        type=str)
    # TODO: prob cant use custom outside of list
    optional.add_argument("--cmap", default="viridis", nargs="?",
                        dest="cmap",
                        help="mpl colormap name.",
                        type=str)
    optional.add_argument("--color",
                        dest="color", help="color for 1D plots and trace plots",
                        widget="ColourChooser")

    # TODO
    # parser.add_argument('--smooth-data', default = None, 
    #                     dest='data_smoothing_level',
    #                     help='Smooth data (plotted as histogram or contour'
    #                             ' levels) using a gaussian filter with sigma='
    #                             'DATA_SMOOTHING_LEVEL.',
    #                     type=float)

    # create optional flag to output everything to console screen
    # TODO: not sure if this works properly
    # optional.add_argument("-ots", "--output_to_screen", default=True,
    #                     dest = "output_to_screen",
    #                     help = "Outputs plot to screen. True (default) or False", 
    #                     action= "store_true") 
    optional.add_argument("-nots", "--no_output_to_screen",
                        dest = "no_output_to_screen",
                        help = "Include this argument to not output the plot to "
                        "your display.", 
                        action= "store_true") 

    # plot tracing arg group
    trace = parser.add_argument_group("Optional Plot Tracing", 
                                       description="Plot a trace on top of the pdist.")
    trace_group = trace.add_mutually_exclusive_group()
    # type to float for val inside tuple, 
    # and nargs to 2 since it is interpreted as a 2 item tuple or list
    trace_group.add_argument("--trace_seg", default=None, nargs=2,
                             dest="trace_seg",
                             help="Trace and plot a single continuous trajectory based"
                                 "off of 2 space-seperated ints : iteration segment",
                             type=int)
    trace_group.add_argument("--trace_val", default=None, nargs=2,
                             dest="trace_val",
                             help="Trace and plot a single continuous trajectory based"
                                  "off of 2 space-seprated floats : Xvalue Yvalue",
                             type=float)
    # TODO: add color option

    ##########################################################
    ############### FORMATTING ARGUMENTS #####################
    ##########################################################

    formatting = parser.add_argument_group("Plot Formatting Arguments") 

    formatting.add_argument("--xlabel", dest="xlabel", type=str)
    formatting.add_argument("--xlim", help="LB UB", dest="xlim", nargs=2, type=float)
    formatting.add_argument("--ylabel", dest="ylabel", type=str)
    formatting.add_argument("--ylim", help="LB UB", dest="ylim", nargs=2, type=float)
    formatting.add_argument("--title", dest="title", type=str)
    formatting.add_argument("--cbar_label", dest="cbar_label", type=str)

    # return the argument parser
    return parser 


# TODO: adjust all to fix str/int/type auto
def handle_command_line(argument_parser): 
    """
    Take command line arguments, check for issues, return the arguments. 

    Parameters
    ----------
    argument_parser : argparse.ArgumentParser 
        The argument parser that is returned in `create_cmd_arguments()`.
    
    Returns
    -------
    argparse.NameSpace
        Contains all arguments passed into EnsembleOptimizer.
    
    Raises
    ------  
    Prints specific issues to terminal.
    """
    # retrieve args
    args = argument_parser.parse_args() 

    # h5 file and file exists
    # if not os.path.exists(args.file) or not ".h5" in args.file:  
    #     # print error message and exits
    #     sys.exit("Must input file that exists and is in .h5 file format.")

    # if not args.percentage.isdigit():  # not correct input   
    #     # print out any possible issues
    #     print("You must input a percentage digit. EXAMPLES: \
    #     \n '-p 40' \n You CANNOT add percent sign (eg. 50%) \n You \
    #     CANNOT add decimals (eg. 13.23)") 
    #     sys.exit(0) # exit program

    # # ignore if NoneType since user doesn't want --maxEnsembleSize parameter
    # if args.max_ensemble_size is None: 
    #     pass

    # elif not args.max_ensemble_size.isdigit(): # incorrect input 
    #     # needs to be whole number
    #     print("You must input a whole number with no special characters (eg. 4).")  
    #     sys.exit(0) # exit program 

    # elif args.max_ensemble_size is '0': # user gives 0 to --maxEnsembleSize flag 
    #     print("You cannot input '0' to --maxEnsembleSize flag.")
    #     sys.exit(0) # exit program 

    return args