class Taper:
    
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Input: Dose, Duration
    # Output: Size, Quantity
    
        
    def calc(self, args):
        phases = []
    
        for k in args:
            dose = args[k].get('dose')
            time = args[k].get('time')
            phases.append(self.rx(dose, time))
    
        
        result = dict.fromkeys(set().union(*phases), 0)

        for d in phases:
            for k in d.keys():
                result[k] += d[k]
        
        return sorted(result.items(), key=lambda x: x[1], reverse=True)
        
        
    def rx(self, dose, days):
        sizes = self.get_sizes(dose)
        return dict((i, (sizes.count(i)) * days) for i in sizes)
        
        
    def get_sizes(self, dose):
        tots = []
        for mg in [50, 20, 10, 5, 2.5, 1]:
            n = dose//mg
            for _ in range(int(n)):
                tots += (str(mg),)
            dose -= mg * n
            if dose == 0.5:
                del tots[-1]
                dose = int(round(mg * n))
            
        return tots
