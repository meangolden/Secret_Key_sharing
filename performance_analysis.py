import matplotlib.pyplot as plt
import numpy as np
from optimal_parameters import prob_matching_keys, exp_missmatches



# plotting
#plot_prob_matching_keys(n_list,  m, alpha):


if __name__ == '__main__':
    '''runs the whole thing, alpha and tau need to be in an array'''
    
    plt.rcParams["font.family"] = 'CMU Sans Serif'  # comment out if problems
    plt.rcParams['font.size'] = 9
    figSize = (4,2)
    fontSize = 9
    
    alpha = 0.1
    m = 256
    n_list = [5,6,7, 8, 9, 10, 11, 12]
    alpha_list = [0.05,.1, .15, .2, .25, .3]
 
    for alpha in alpha_list:
        
        #plot_KDR(n_list, alpha):
        plt.figure(figsize = figSize)
        for tau in range(int(max(n_list)/3)-1):
            ys= []
            #probMismatch = []
            for n in n_list:
                if tau <= (np.ceil(n/2)-1):
                    y= exp_missmatches(n, tau, 10 , alpha)/10
                    ys.append(y)
            l = len(ys)     
            plt.plot(n_list[-l:], ys, '--o', label= r'$\tau$ = {}'.format(tau))
        #plt.plot(n_list, probMismatch, label='key mismatch prob')
        plt.xticks(n_list, fontsize = fontSize)
        plt.xlabel('Block size length', fontsize = fontSize)
        plt.ylabel('KDR', fontsize = fontSize)
        plt.title(r'$\alpha$= {}'.format(alpha), fontsize = fontSize)
        plt.grid()
        plt.legend(fontsize = fontSize)
        plt.savefig(f"plot/KDR_alp{alpha}_m{m}.pdf", format="pdf", bbox_inches="tight")
        plt.savefig(f"plot/KDR{alpha}_m{m}.eps", format="eps",bbox_inches="tight")
