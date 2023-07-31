from typing import List


class DynamicAccessNestedDict:
    """Dynamically get/set nested dictionary keys of 'data' dict"""

    def __init__(self, data: dict):
        self.data = data

    def getval(self, keys: List):
        data = self.data
        for k in keys:
            if k.isdigit():
                k = int(k)

            data = data[k]
        return data

    def setval(self, keyString, val) -> None:

        def convertStar(strings):
            newStrings = []
            for thing in strings:
                if "*" not in thing:
                    newStrings.append(thing)
                    continue

                split = thing.split('.')
                index = split.index("*")
                temp = split[:index]
                length = len(self.getval(temp))
                for i in range(0, length):
                    # print('key' + thing.replace("*", str(i)))
                    # print('list of strings to convert' + strings)
                    # print('retrieved value' + self.getval(temp))
                    # print('key split' + split)
                    # print('key' + thing)
                    # print(temp)
                    # print(length)
                    newStrings.append(thing.replace("*", str(i), 1))
                    # print(newStrings)
                    # print(strings)
            if newStrings == strings:
                return newStrings

            return convertStar(newStrings)

        keyStrings = convertStar([keyString])
        for value in keyStrings:
            data = self.data
            keys = value.split('.')
            lastkey = keys[-1]
            for k in keys[:-1]:  # when assigning drill down to *second* last key
                if k.isdigit():
                    k = int(k)

                # print(value)
                # print(data)
                # print(k)
                data = data[k]


            data[lastkey] = val
