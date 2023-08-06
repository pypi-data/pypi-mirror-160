class BeadsVec:
    """Beads Nested Number"""

    def __init__(self, value=0):

        # 整数かどうか判定
        try:
            int_value = int(str(value), 10)
        except ValueError:
            # 整数でなければ次へ
            pass
        else:
            # タプルとして格納する
            self._elements = int_value,
            return

        # タプル型なら
        if type(value) is tuple:
            # そのまま入れる
            self._elements = value
            return

        # それ以外は文字列として扱う

        # 大文字に変換
        text = value.upper()

        new_element_list = []

        # 区切り文字 'O' で分割
        tokens = text.split('O')

        for token in tokens:
            # 整数かどうか判定
            try:
                int_element = int(str(token), 10)
                new_element_list.append(int_element)

            except ValueError:
                # 整数でなければ
                raise ValueError(f"no beads vector notation: {value}")

        # タプルとして格納する
        self._elements = tuple(new_element_list)

    def __str__(self):
        """数珠玉記数法"""
        text = ""
        for token in self._elements:
            text = f"{text}o{token}"

        # 先頭の 'o' は除去します
        return text.lstrip('o')

    @property
    def elements(self):
        return self._elements
