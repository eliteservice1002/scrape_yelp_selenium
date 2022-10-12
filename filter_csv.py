import csv
from os import listdir
from os.path import isfile, join
def main():
    # get file names
    onlyfiles = [f for f in listdir("./csv/") if isfile(join("./csv/", f))]
    print(u'fils:{0}'.format(len(onlyfiles)))

    # write header
    FIELD_NAME = ["title", "campUrl", "about", "category", "picture", "location", "city", "zipcode", "contact", "siteUrl", "additional"]
    with open('filterd_data_daynight.csv', "w",encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=FIELD_NAME )
        writer.writeheader()

    #check duplicate
    for file in onlyfiles:
        print(u'check duplicate from {0} and filter & write in {1}'.format(file,'filterd_data_daynight.csv'))
        with open("./csv/"+file, 'r') as in_file, open('filterd_data_daynight.csv', 'a') as out_file:
            seen = set()  # set for fast O(1) amortized lookup
            for line in in_file:
                if line in seen:
                    continue  # skip duplicate

                seen.add(line)
                out_file.write(line)
        print(u'done')

        # with open("filterd_data1.csv", 'r') as in_file, open('filterd_data.csv', 'a') as out_file:
        #     seen = set()  # set for fast O(1) amortized lookup
        #     for line in in_file:
        #         if line in seen:
        #             continue  # skip duplicate

        #         seen.add(line)
        #         out_file.write(line)
# main entry
if __name__ == '__main__':
    main()