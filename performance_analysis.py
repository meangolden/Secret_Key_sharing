import matplotlib.pyplot as plt
import numpy as np
from optimal_parameters import exp_missmatches, tx_key_rate



# plotting
#plot_prob_matching_keys(n_list,  m, alpha):


if __name__ == '__main__':
    '''runs the whole thing, alpha and tau need to be in an array'''
    
    plt.rcParams["font.family"] = 'CMU Sans Serif'  # comment out if problems
    plt.rcParams['font.size'] = 9
    figSize = (4,2)
    fontSize = 9
    
    m = 128
    n_list = [5,6,7, 8, 9, 10,11,12]
    alpha_list = [0.01, 0.05,.1, .15, .2, .25, .3, 0.4]
 
    for alpha in alpha_list:
        
        #plot_KDR(n_list, alpha):
        plt.figure(figsize = figSize)
        for tau in range(int(max(n_list)/3)-1):
            ys= []
            #probMismatch = []
            for n in n_list:
                if tau <= (np.ceil(n/2)-1):
                    y= exp_missmatches(n, tau, alpha, 10)/10
                    ys.append(y)
            l = len(ys)     
            plt.plot(n_list[-l:], ys, '--o', label= r'$\tau$ = {}'.format(tau))
            
        plt.xticks(n_list, fontsize = fontSize)
        plt.xlabel('Blocksize (n)', fontsize = fontSize)
        plt.ylabel('KDR', fontsize = fontSize)
        plt.title(r'$p$ch= {}'.format(alpha), fontsize = fontSize)
        plt.grid()
        plt.legend(fontsize = fontSize)
        plt.savefig(f"plot/KDR_alp{alpha}.pdf", format="pdf", bbox_inches="tight")
        plt.savefig(f"plot/KDR{alpha}.eps", format="eps",bbox_inches="tight")

 

        plt.figure(figsize = figSize)
        for tau in range(int(max(n_list)/3)-1):
            ys= []
            #probMismatch = []
            for n in n_list:
                if tau <= (np.ceil(n/2)-1):
                    y= tx_key_rate(n, tau, alpha)
                    ys.append(y)
            l = len(ys)
            
            plt.plot(n_list[-l:], ys, '--o', label= r'$\tau$ = {}'.format(tau))

        plt.xticks(n_list, fontsize = fontSize)
        plt.xlabel('Blocksize (n)', fontsize = fontSize)
        plt.ylabel('R', fontsize = fontSize)
        plt.title(r'$p$ch= {}'.format(alpha), fontsize = fontSize)
        plt.grid()
        plt.legend(fontsize = fontSize)
        plt.savefig(f"plot/KTR_alp{alpha}.pdf", format="pdf", bbox_inches="tight")
        plt.savefig(f"plot/KTR{alpha}.eps", format="eps",bbox_inches="tight")