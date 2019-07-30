import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from buildingspy.io.outputfile import Reader

cases = ["betonRoof", "glassRoof"]
#cases = ["airRes", "glassRes"]


def quick_plot(x, y, x_label, y_label, fig_name):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(fig_name)
    plt.clf()


def plot_variable(var, x_label, file_name, var_modifier=0.0):
    mat_file = "case_" + case + ".mat"
    # PLOT
    r = Reader(os.path.join("output", mat_file), "dymola")
    (t, y) = r.values(var)
    quick_plot(t, [x + var_modifier for x in y], x_label, var, file_name)


def split_plot_variable(var, s, e, x_label, file_name, var_modifier=0.0):
    mat_file = "case_" + case + ".mat"
    # PLOT
    r = Reader(os.path.join("output", mat_file), "dymola")
    (t, y) = r.values(var)
    t = t[s:e]
    y = y[s:e]
    quick_plot(t, [x + var_modifier for x in y], x_label, var, file_name)

def getCases():
    with open("cases.json", "r") as f:
        data = json.load(f)
    return data

def main():
        jsonData = getCases()
        for (caseName, data) in jsonData.iteritems():
            # plot totalPowerLoad for each subcase of each case
            params = data[0].iteritems()
            # simulate for each set of variables
            subCaseAmount = len(params.next()[1])
            print("plotting " + str(subCaseAmount) + " subcases for case: " + caseName)
            plt.figure()
            for currentSubCase in range(subCaseAmount):
                print(str(currentSubCase + 1) + "/" + str(subCaseAmount))

                matFile = caseName + "_"
                plotLabel = data[1]
                variables = []
                for (varName, valueList) in data[0].iteritems():
                    value = valueList[currentSubCase]
                    matFile += varName + "_" + str(value)
                    plotLabel += "_" + str(value)
                    variables.append(varName)

                fileReader = Reader(os.path.join("output_" + caseName, matFile.replace(".","_") + ".mat"), "dymola")
                (t, y) = fileReader.values("totalPowerLoad")
                # seconds to days
                t = [x / 86400 for x in t]
                plt.plot(t, y, label=plotLabel)
            plt.xlabel("Time [d]")
            plt.ylabel("MWh")
            plt.legend()
            if not os.path.exists("plot_" + caseName):
                os.makedirs("plot_" + caseName)
            plt.savefig("plot_" + caseName + "/totalPowerLoad")



if __name__ == '__main__':
    main()
