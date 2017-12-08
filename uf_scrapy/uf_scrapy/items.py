class UF:

    @staticmethod
    def prepend_zero(x):
        if x < 10:
            return "0" + str(x)
        return str(x)

    @staticmethod
    def create(y, m, d, value):
        date = "{}-{}-{}".format(y, UF.prepend_zero(m), UF.prepend_zero(d))
        value = float(value.replace('.', '').replace(',', '.'))
        return {"date": date, "value": value}
