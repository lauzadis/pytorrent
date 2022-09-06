from pytorrent import bencode

class TestBencodeEncode:

    def test_string(self):
        s = "hello"
        assert bencode.encode(s) == "5:hello"

    def test_int(self):
        i = 2923
        assert bencode.encode(i) == "i2923e"

    def test_list(self):
        l = ["hello", "this", "is", "a", "list", 10293]

        assert bencode.encode(l) == "l5:hello4:this2:is1:a4:listi10293ee"

    def test_dict(self):
        d = {
            "hello": "world",
            "answer_to_universe": 42,
            "order": ["borger", "fri"]
        }

        assert bencode.encode(d) == "d5:hello5:world18:answer_to_universei42e5:orderl6:borger3:friee"

class TestBencodeDecode():

    def test_string(self):
        s = "5:hello"
        res, length = bencode.decode(s)

        assert length == len(s) and res == "hello"

    def test_int(self):
        i = "i2923e"
        res, length = bencode.decode(i)

        assert length == len(i) and res == 2923

    def test_list(self):
        l = "l5:hello4:this2:is1:a4:listi10293ee"
        res, length = bencode.decode(l)

        assert length == len(l) and res == ["hello", "this", "is", "a", "list", 10293]

    def test_dict(self):
        d = "d5:hello5:world18:answer_to_universei42e5:orderl6:borger3:friee"
        res, length = bencode.decode(d)

        assert length == len(d) and res == {
            "hello": "world",
            "answer_to_universe": 42,
            "order": ["borger", "fri"]
        }
