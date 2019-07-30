from buildingspy.simulate.Simulator import Simulator
import json

ideasPackagePath = "C:\Program Files\Dymola 2019 FD01\Modelica\IDEAS 2.1.0"
thermalResistance = "thermalZoneFourElements.RWin"
thermalResistanceExt = "thermalZoneFourElements.RExt"
peopleAmplitude = "people.amplitude"

def getCases():
    with open("cases.json", "r") as f:
        data = json.load(f)
    return data
    # parameter_variations = {"WindowThermalResistance": ("thermalZoneFourElements.RWin", [0.0, 0.1, 0.2, 0.3, 0.4]) }

def simulate(s):
    # SIMULATE
    s.setStopTime(3600 * 24 * 365)
    s.simulate()

def main():
    jsonCases = getCases()
    for (caseName, data) in jsonCases.iteritems():
        params = data[0].iteritems()
        # simulate for each set of variables
        subCaseAmount = len(params.next()[1])
        print("simulating " + str(subCaseAmount) + " subcases for case: " + caseName)
        for currentSubCase in range(subCaseAmount):
            print(str(currentSubCase+1) + "/" + str(subCaseAmount))
            simulation = Simulator("MyFourElements", "dymola",
                                   packagePath=ideasPackagePath,
                                   outputDirectory="output_" + caseName)
            resultFileName = caseName + "_"
            for (varName, valueList) in data[0].iteritems():
                value = valueList[currentSubCase]
                simulation.addParameters({varName: value})
                resultFileName += varName + "_" + str(value)
            simulation.setResultFile(resultFileName.replace(".", "_"))
            simulate(simulation)

if __name__ == '__main__':
    main()
