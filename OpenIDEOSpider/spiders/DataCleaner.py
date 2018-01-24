import pandas as pd

df = pd.read_csv(r'NewData.csv')

new_list = df['Geolocation'].tolist()


"""for val in new_list:"""

count1 = 0
while count1 < len(new_list):
    comma_index = 0
    count = 0
    while count < len(new_list[count1]):
        if new_list[count1][count] == ',':
            comma_index = count
        count += 1
    if comma_index == 0:
        new_list[count1] = new_list[count1]
    else:
        new_list[count1] = new_list[count1][comma_index + 2:]
    count1 += 1

countries = {}

for thing in new_list:
    if not thing in countries:
        countries[thing] = [1]
    else:
        countries[thing].append(1)

print(countries)
