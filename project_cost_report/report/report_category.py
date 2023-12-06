from odoo.tools.float_utils import float_round


class CostReportCategory:
    """Cost report category.

    This class is used to simplify the qWeb templates.
    It contains the data related to a category of the report.
    """

    def __init__(self, section, category, lines, folded):
        self.section = section
        self.category = category
        self.id = category.id
        self.name = category.name
        self.lines = lines
        self.folded = folded
        self.cost = float_round(sum(-l.amount for l in lines if not l.revenue), 2)
        self.revenue = float_round(sum(l.amount for l in lines if l.revenue), 2)
        self.profit = float_round((self.revenue - self.cost), 2)

    @property
    def total_hours(self):
        return float_round(sum(l.unit_amount for l in self.lines if not l.revenue), 2)

    @property
    def target_type(self):
        return self.category.target_type

    @property
    def target_margin(self):
        return self.category.target_margin

    @property
    def target_hourly_rate(self):
        return self.category.target_hourly_rate

    @property
    def target_sale_price(self):
        if self.category.target_type == "hourly_rate":
            return float_round(self.total_hours * self.target_hourly_rate, 2)
        else:
            sale_price_ratio = 1 - self.target_margin / 100
            return float_round(
                self.cost / sale_price_ratio if sale_price_ratio else 0, 2
            )

    @property
    def target_profit(self):
        return float_round(self.target_sale_price - self.cost, 2)
