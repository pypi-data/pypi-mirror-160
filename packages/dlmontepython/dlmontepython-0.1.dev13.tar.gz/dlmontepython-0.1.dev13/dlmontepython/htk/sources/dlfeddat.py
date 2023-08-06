"""
Class corresponding to a data container for data in DL_MONTE's FEDDAT files.

"""

import os


class FEDDAT(object):

    """
    Container for data contained in the FEDDAT files.
    """

    def __init__(self, data):

        """Initialise the data in the container"""

        self.data = data


    def __str__(self):
        
        """Return a string representation of the FEDDAT data.
        
        Returns a string representation of the FEDDAT data.
        The format of the string is similar, though not identical to, the format of
        the FEDDAT files output by DL_MONTE. For FEDDAT objects containing multiple
        iterations of data the data corresponding to each iteration is output in
        turn, such that the string looks like concatenated DL_MONTE FEDDAT files.       
        """

        lines = []

        # Loop over FEDDAT iterations and output in FEDDAT-file format
        # for each iteration, concatenating the data for each iteration
        for i in range(len(self.data)):
            lines.append("# FEDDAT data from dlfeedat, iteration {}".format(i))
            lines.append("#")
            lines.append("# param   bias   hist")
            for j in range(len(self.data[i]["param"])):
                lines.append("{} {} {}".format(self.data[i]["param"][j],self.data[i]["bias"][j],self.data[i]["hist"][j]))

        return "\n".join(lines)



    def param(self, iteration=-1):

        """Return the order parameter array

        Return the order parameter array.

        Parameters
        ----------
        iteration : int
                    FEDDAT file number of the order parameter array: 'iteration'
                    maps to the '(iteration+1)'th FEDDAT file. E.g. if 'iteration'
                    were 0 then the array returned corresponds to 'FEDDAT.000_001'.
                    Similarly 5 corresponds to 'FEDDAT.000_006'; -1 (default) 
                    corresponds to the FEDDAT file with the highest index; -2 
                    corresponds to the FEDDAT file with the 2nd highest index, etc.

        Returns
        -------
        array
            Array containing the order parameter grid points for the specified FEDDAT 
            iteration.

        """
        return self.data[iteration]["param"]



    def bias(self, iteration=-1):

        """Return the bias array

        Return the (by default the most recent) bias array.

        Arguments
        ---------
        iteration : int
            FEDDAT file number of the bias array: 'iteration'
            maps to the '(iteration+1)'th FEDDAT file. E.g. if 'iteration'
            were 0 then the array returned corresponds to 'FEDDAT.000_001'.
            Similarly 5 corresponds to 'FEDDAT.000_006'; -1 (default) 
            corresponds to the FEDDAT file with the highest index; -2 
            corresponds to the FEDDAT file with the 2nd highest index, etc.

        Returns
        -------
        array
            Array containing the biases / bias function for the specified FEDDAT iteration.

        """

        return self.data[iteration]["bias"]



    def hist(self, iteration=-1):

        """Return the histogram array.

        Return the (by default the most recent) histogram array.

        Arguments
        ---------
        iteration : int
            FEDDAT file number of the histogram array: 'iteration'
            maps to the '(iteration+1)'th FEDDAT file. E.g. if 'iteration'
            were 0 then the array returned corresponds to 'FEDDAT.000_001'.
            Similarly 5 corresponds to 'FEDDAT.000_006'; -1 (default) 
            corresponds to the FEDDAT file with the highest index; -2 
            corresponds to the FEDDAT file with the 2nd highest index, etc.

        Returns
        -------
        array
            Array containing the histogram for the specified FEDDAT iteration.

        """

        return self.data[iteration]["hist"]



def load(directory=os.curdir):

    """Load contents of the FEDDAT files

    Load contents of the FEDDAT files.

    Arguemnts
    ---------
    directory : string
        Location of the FEDDAT files, which by default is the current directory.

    Returns
    -------
    data : FEDDAT
        Object containing data corresponding to the FEDDAT files in the specified
        directory.
    """

    data = []

    # Loop over FEDDAT.000_??? files
    for i in range(1,999):

        istring = f'{i:03d}'
        filename = "FEDDAT.000_"+istring

        if os.path.exists(os.path.join(directory,filename)):
            # Read data from the files. The file format is 3 comment lines followed
            # by N lines of data, where each line contains the order parameter (param),
            # free energy (fe) and histogram count (hist)
            param = []
            bias = []
            hist = []
            with open(filename, "r") as filecontext:
                # Skip the first 3 lines
                for line in filecontext.readlines()[3:]:
                    values =  [float(val) for val in line.strip().split()]
                    param.append(values[0])
                    bias.append(values[1])
                    hist.append(values[2])

            idata = dict([('param',param),('bias',bias),('hist',hist)])
            data.append(idata)

        else:

            break

    return FEDDAT(data)
