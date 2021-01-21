class TransportConfig:
    def __init__(self) -> None:
        self.dict = dict()

    def get_var(self, key):
        if key in self.dict:
            return self.dict[key]
        return None


#<form method="post">
#    <input type="text" name="username" />
#    <input type="text" name="password" />
#    <input type="submit" value="" />
#</form>