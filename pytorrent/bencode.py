def encode(data, bencoded=""):

    if isinstance(data, dict):
        bencoded += "d"

        for key in data.keys():
            bencoded += encode(key)
            bencoded += encode(data[key])
        
        bencoded += "e"

    if isinstance(data, list):
        bencoded += "l"

        for item in data:
            bencoded += encode(item)

        bencoded += "e"

    if isinstance(data, str):
        bencoded += f"{len(data)}:{data}"

    if isinstance(data, int):
        bencoded += f"i{data}e"

    return bencoded

def decode(bencoded, i=0):
    if bencoded is None: return
    
    if bencoded[i] == "i":
        end = bencoded[i:].find("e")
        return int(bencoded[i+1:i+end]), i + end + 1

    elif bencoded[i] == "l":
        l = []
        i += 1  # eat the 'l'

        while bencoded[i] != "e":
            val, i = decode(bencoded, i)
            l.append(val)
        i += 1  # 'e'
        
        return l, i

    elif bencoded[i] == "d":
        d = {}
        i += 1

        while bencoded[i] != "e":
            key, i = decode(bencoded, i)
            val, i = decode(bencoded, i)
            print(key, val)
            d[key] = val

        i += 1

        return d, i
            
    else:
        length = int(bencoded[i : i + bencoded[i:].find(":")])
        return str(bencoded[i+1+len(str(length)) : i+1+len(str(length))+length]), i + 1 + len(str(length)) + length
