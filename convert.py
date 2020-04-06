import shutil
import sys
from itertools import count
import os

def main():
    args = len(sys.argv)

    if args < 2:
        print("Use as convert.py input.csv ./output-folder/")
        exit(0)

    print("Opening "+sys.argv[1]+" and writing to "+sys.argv[2])
    input_file = open(sys.argv[1], "r")
    output_directory = sys.argv[2]
    if not output_directory.endswith("/"):
        output_directory += "/"

    # clear output
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    line_count = 0
    lines = input_file.readlines()
    for line in lines:
        line_count += 1
        if line_count == 1:
            continue

        variables = line.split(",")
        variable_count = len(variables)

        # remove trailing newlines
        for i in (0, variable_count-1):
            variables[i] = variables[i].rstrip()

        idx = 0
        filename = variables[idx]
        idx += 1
        sname = variables[idx]
        idx += 1
        sgroup = variables[idx]
        idx += 1
        fname = variables[idx]
        idx += 1
        ftectonicRegion = variables[idx]
        idx += 1
        fid = variables[idx]
        idx += 1
        faValue = variables[idx]
        idx += 1
        fbValue = variables[idx]
        idx += 1
        fminMag = variables[idx]
        idx += 1
        fmaxMag = variables[idx]
        idx += 1
        frake = variables[idx]
        idx += 1

        # parse XY values
        variable_list = ""
        while idx < variable_count-3:
            variable_list += variables[idx]+" "
            idx += 1

        fdip = variables[idx]
        idx += 1
        fupperSeismoDepth = variables[idx]
        idx += 1
        flowerSeismoDepth = variables[idx]
        idx += 1

        template = """
            <?xml version="1.0" encoding="UTF-8"?>
            <nrml xmlns:gml="http://www.opengis.net/gml" xmlns="http://openquake.org/xmlns/nrml/0.5">
            <sourceModel name="{sname}">
                <sourceGroup name="{sgroup}">
                    <characteristicFaultSource name="{fname}" tectonicRegion="{ftectonicRegion}" id="{fid}">
                        <truncGutenbergRichterMFD aValue="{faValue}" bValue="{fbValue}" minMag="{fminMag}" maxMag="{fmaxMag}" />
                        <rake>"{frake}"</rake>
                        <surface>
                            <simpleFaultGeometry>
                                <gml:LineString>
                                    <gml:posList>
                                        {variable_list}
                                    </gml:posList>
                                <gml:LineString>
                                <dip>"{fdip}"</dip>
                                <upperSeismoDepth>"{fupperSeismoDepth}"</upperSeismoDepth>
                                <lowerSeismoDepth>"{flowerSeismoDepth}"</lowerSeismoDepth>
                            </simpleFaultGeometry>
                        </surface>
                    </characteristicFaultSource>
                </sourceGroup>
            </sourceModel>
            </nrml>
        """
        converted = template.format(
            sname=sname,
            sgroup=sgroup,
            fname=fname,
            ftectonicRegion=ftectonicRegion,
            fid=fid,
            faValue=faValue,
            fbValue=fbValue,
            fminMag=fminMag,
            fmaxMag=fmaxMag,
            frake=frake,
            variable_list=variable_list.strip(),
            fdip=fdip,
            fupperSeismoDepth=fupperSeismoDepth,
            flowerSeismoDepth=flowerSeismoDepth
        )

        output_filename = output_directory + filename + ".xml"
        print("Writing to "+output_filename+"...")
        output = open(output_filename, "w+")
        output.writelines(converted)
        output.close()

    input_file.close()

    print("Done!")

if __name__ == '__main__':
    main()




