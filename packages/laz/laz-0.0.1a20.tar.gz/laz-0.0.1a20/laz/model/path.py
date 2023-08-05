class Path:

    def __init__(
            self,
            value: str,
            default_base_path: str,
            default_target: str,
            path_delimiter: str,
            **_,
    ):
        self.value = value if path_delimiter in value else f'{path_delimiter}{value}'
        self.default_base_path = default_base_path
        self.default_target = default_target
        self.path_delimiter = path_delimiter

    def __repr__(self):
        return self.value

    @property
    def base(self) -> str:
        return self.value.split(self.path_delimiter)[0] or self.default_base_path

    @base.setter
    def base(self, new_base: str):
        self.value = self.value.replace(self.base, new_base)

    @property
    def target(self) -> str:
        return self.value.split(self.path_delimiter)[-1] or self.default_target

    @property
    def base_pattern(self) -> str:
        if self.base == '':
            return '**'
        else:
            return f'**/{self.base}/**'
