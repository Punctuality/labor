import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def yes_check(phrase):
    ans = input("\n"+phrase)
    ans = ans.lower()
    trues = ['y', 'yes', 'yep', 'ya', '', '\n']
    if ans in trues:
        return True
    return False

def make_list(file_existance):
    if file_existance:
        print('\n')
        path = input("Please, enter your file's path: ")
        file = open(path, "r")
        lines = file.readlines()
        lines = [[int(lines[x].split("\t")[j]) for j in range(len(lines[x].split("\t"))) if j < 2 and lines[x].split("\t")[j] not in ["", "\n"] ] for x in range(len(lines))]
        lines = [x for x in lines if x not in [ [], None, ""]]
        df = pd.DataFrame(columns=["Up_Mean", "Down_Mean", "Rpm"])
        up = []
        dwn = []
        rpm = []
        u = []
        d = []
        for i in lines:
            if len(i) == 1:
                rpm.append(i[0])
                if u != [] and d != []:
                    up.append(np.mean(u))
                    dwn.append(np.mean(d))
                    u = []
                    d = []
            else:
                u.append(i[0])
                d.append(i[1])
        up.append(np.mean(u))
        dwn.append(np.mean(d))            
        df.Up_Mean = up
        df.Down_Mean = dwn
        df.Rpm = rpm
        return df
    else:
        inp = input("Input your origin data here: ")
        return inp

def save_df(data_frame):
    path = input("Enter path for saving DataFrame (with out ./format): ")
    try:
        data_frame.to_excel(path+".xlsx")
    except:
        return False
    return True
    

def alph_check(alpha, Rpm, a, d):
    if alpha[a][1] < 0.12:
        return False
    dif_max = abs(alpha[a][2]-alpha[a][1])
    dif_min = abs(alpha[a][0]-alpha[a][1])
    dif = abs(dif_max - dif_min)
    if dif > 0.15:
        return False
    return True
    
def plot_char(data_frame):
    ans = input("X-axis: 1-Down, 2-Up: ")
    alph = []
    
    if ans == '1':
        alph = [abs(data_frame.Down_Mean[i])/(data_frame.Rpm[i])**2 for i in range(1, len(data_frame.Rpm))]
        alph.append([np.min(alph[1:-1]), np.mean(alph[1:-1]), np.max(alph[1:-1])])
    elif ans == '2':
        alph = [abs(data_frame.Up_Mean[i])/(data_frame.Rpm[i])**2 for i in range(1, len(data_frame.Rpm))]
        alph.append([np.min(alph[1:-1]), np.mean(alph[1:-1]), np.max(alph[1:-1])])
    else:
        print('You have entered incorrect value.')
    l_d = len(data_frame)- 1
    l_a = len(alph) - 1
    print("Is coefficent normal? (Beta) : " + str(alph_check(alph, data_frame.Rpm[1:], l_a, l_d)))
    
    plt.subplot(122)
    plt.scatter(data_frame.Rpm, np.abs(data_frame.Up_Mean), c = 'r')
    plt.plot(data_frame.Rpm, np.abs(data_frame.Up_Mean), c = 'black', label = 'Up')
    plt.legend(loc='upper left', frameon=False)
    plt.subplot(121)
    plt.scatter(data_frame.Rpm, np.abs(data_frame.Down_Mean), c = 'b')
    plt.plot(data_frame.Rpm, np.abs(data_frame.Down_Mean), c = 'black', label = 'Down')
    plt.suptitle("Force/Rpm")
    plt.legend(loc='upper left', frameon=False)
    plt.show()
    plt.suptitle('Alpha/Rpm')
    plt.scatter(data_frame.Rpm[1:], alph[:-1], c = 'green', label = "Data Points")
    plt.plot(data_frame.Rpm[1:], alph[:-1], c = 'black', label = "Alpha tradeline")
    plt.plot([data_frame.Rpm[1], data_frame.Rpm[l_d]], [alph[l_a][0], alph[l_a][0]], c = 'r', label = 'Min ('+str(alph[l_a][0])+")")
    plt.plot([data_frame.Rpm[1], data_frame.Rpm[l_d]], [alph[l_a][1], alph[l_a][1]], c = 'r', label = 'Mean ('+str(alph[l_a][1])+")")
    plt.plot([data_frame.Rpm[1], data_frame.Rpm[l_d]], [alph[l_a][2], alph[l_a][2]], c = 'r', label = 'Max ('+str(alph[l_a][2])+")")
    plt.legend(loc='lower right', frameon=False)
    plt.show()
    
    
def startup():
    print("This sketch'll help you to optimize your time\nhelping with work on this tenso-weights.")
    #ans = (yes_check("Have you got a file with your origin data? [Y/n] "))
    data_frame = make_list(True)
    print("\nParsed Data: ")
    print(data_frame)
    ans = yes_check("Do you want to save it? [Y/n] ")
    if ans:
        if save_df(data_frame):
            print("Saved.")
        else:
            print("Some problem encoured.")
    ans = yes_check("Do you want to pre-plot motor chars? [Y/n] ")
    if ans:
        plot_char(data_frame)


startup()