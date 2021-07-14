from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

auto_attack_speed = 0.7
cast_speed = 1/0.5
ult_and_auto_cast_speed = 1/2.0

auto_attack_time = 1/0.7
cast_time = 0.5
ult_and_auto_cast_time = 2.0

max_time = 20
time_array_length = 200
time_array = np.linspace(0, max_time, time_array_length)
crit_multiplier = 1.3
crit_rate = 0.25
crit_dmg = crit_multiplier*crit_rate
karma_ult_damage = 280

karma_autos_nothing = [5, 4, 2]
karma_autos_1mana = [4, 4, 2]
karma_autos_2mana = [2, 4, 2]
karma_autos_shojin = [2, 2, 2]
karma_autos_bb = [2, 2, 1]

karma_autos_2inv_nothing = [4, 3, 2]
karma_autos_2inv_1mana = [3, 3, 2]
karma_autos_2inv_2mana = [2, 3, 2]
karma_autos_2inv_shojin = [2, 2, 1]
karma_autos_2inv_bb = [2, 2, 1]
karma_autos_2inv_bb_1mana = [1, 2, 1]
karma_autos_2inv_bb_2mana = [0, 2, 1]

# fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
# fig.set_size_inches(17, 10)

def make_dmg_array(autos_array, ap_scaling=1.0, crit_multiplier=1.0, ap_increase_per_cast=(0, 0, 0)):
    karma_tpc = [autos_array[0]*auto_attack_time+cast_time, autos_array[1]*auto_attack_time+cast_time, autos_array[2]*auto_attack_time+cast_time]

    i = 0
    karma_dmg = np.array([])
    temp_damage = 0
    # if karma_tpc[0] == 0.5:
    #     karma_tpc[0] = 0
    for i in range(int(np.floor(karma_tpc[0] * 10))):
        temp_damage += karma_ult_damage * ap_scaling * crit_multiplier * (1 / int(np.floor(karma_tpc[0] * 10)))
        karma_dmg = np.append(karma_dmg, [temp_damage])
    for i in range(int(np.floor(karma_tpc[1] * 10))):
        temp_damage += (karma_ult_damage * (ap_scaling + ap_increase_per_cast[0]) * crit_multiplier) * (1 / int(np.floor(karma_tpc[1] * 10)))
        karma_dmg = np.append(karma_dmg, [temp_damage])
    for i in range(int(np.floor(karma_tpc[2] * 10))):
        temp_damage += 3*(karma_ult_damage * (ap_scaling + ap_increase_per_cast[1]) * crit_multiplier) * (1 / int(np.floor(karma_tpc[2] * 10)))
        karma_dmg = np.append(karma_dmg, [temp_damage])

    i = 0
    initial_length = len(karma_dmg)
    ap_increase_per_cast_new = ap_increase_per_cast[2]
    temp_damage = karma_dmg[-1]
    while i < (time_array_length-initial_length):
        if i % 20 == 0 and not ap_increase_per_cast[0] == 0:
            ap_increase_per_cast_new += 0.10*0.45

        temp_damage += (5/3) * karma_ult_damage * (ap_scaling + ap_increase_per_cast_new) * crit_multiplier * (1 / 20)
        karma_dmg = np.append(karma_dmg, [temp_damage])
        i += 1

    return karma_dmg


def make_compare_mana():
    karma_dmg_nothing = make_dmg_array(karma_autos_2inv_nothing)
    karma_dmg_shojin = make_dmg_array(karma_autos_2inv_shojin)
    karma_dmg_bb = make_dmg_array(karma_autos_2inv_bb)
    karma_dmg_1mana = make_dmg_array(karma_autos_2inv_1mana)
    karma_dmg_2mana = make_dmg_array(karma_autos_2inv_2mana)

    fig1, (ax1, ax2) = plt.subplots(1, 2)
    fig1.set_size_inches(12, 5)

    ax1.plot(time_array, karma_dmg_nothing, label='nothing')
    ax1.plot(time_array, karma_dmg_shojin - 25, label='shojin')
    ax1.plot(time_array, karma_dmg_bb, label='BB')
    ax1.plot(time_array, karma_dmg_1mana, label='1 mana')
    ax1.plot(time_array, karma_dmg_2mana, label='2 mana')
    ax1.set_xlabel('time (s)')
    ax1.set_title('Comparison of mana items - Damage vs. Time')
    ax1.legend()

    ax2.plot(time_array, np.gradient(karma_dmg_nothing), label='nothing')
    ax2.plot(time_array, np.gradient(karma_dmg_shojin)-0.2, label='shojin')
    ax2.plot(time_array, np.gradient(karma_dmg_bb), label='BB')
    ax2.plot(time_array, np.gradient(karma_dmg_1mana), label='1 mana')
    ax2.plot(time_array, np.gradient(karma_dmg_2mana), label='2 mana')
    ax2.set_xlabel('time (s)')
    ax2.set_title('Comparison of mana items - DPS vs. Time')
    ax2.legend()

    plt.show()


def make_compare_bis():
    karma_dmg_blue_dcap_jg = make_dmg_array(karma_autos_2inv_bb, ap_scaling=1.8, crit_multiplier=(0.6*1.0 + 0.4*1.7)) # Blue, Dcap, JG
    karma_dmg_blue_ie_jg = make_dmg_array(karma_autos_2inv_bb, ap_scaling=1.1, crit_multiplier=1.0*1.85)  # Blue, IE, JG
    karma_dmg_dcap_ie_jg = make_dmg_array(karma_autos_2inv_nothing, ap_scaling=1.9, crit_multiplier=1.0*1.85) # Dcap, IE, JG
    karma_dmg_blue_dcap_as = make_dmg_array(karma_autos_2inv_bb_1mana, ap_scaling=1.8, crit_multiplier=1.0, ap_increase_per_cast=(0.35*0.45, (0.35+0.2)*0.45, (0.35+0.2+0.1)*0.45)) # Blue, Dcap, AS
    karma_dmg_blue_jg_as = make_dmg_array(karma_autos_2inv_bb_1mana, ap_scaling=1.2, crit_multiplier=(0.6*1.0 + 0.4*1.7), ap_increase_per_cast=(0.35*0.45, (0.35+0.2)*0.45, (0.35+0.2+0.1)*0.45)) # Blue, JG, AS
    karma_dmg_blue_hoj_as = make_dmg_array(karma_autos_2inv_bb_2mana, ap_scaling=1.45, crit_multiplier=1.0, ap_increase_per_cast=(0.35*0.45, (0.35+0.2)*0.45, (0.35+0.2+0.1)*0.45)) # Blue, HOJ, AS

    fig2, (ax3, ax4) = plt.subplots(1, 2)
    fig2.set_size_inches(12, 5)

    ax3.plot(time_array, karma_dmg_blue_dcap_jg, label='BB Dcap JG')
    ax3.plot(time_array, karma_dmg_blue_ie_jg, label='BB IE JG')
    ax3.plot(time_array, karma_dmg_dcap_ie_jg, label='Dcap IE JG')
    ax3.plot(time_array, karma_dmg_blue_dcap_as, label='BB Dcap AS')
    ax3.plot(time_array, karma_dmg_blue_jg_as, label='BB JG AS')
    ax3.plot(time_array, karma_dmg_blue_hoj_as, label='BB HOJ AS')
    ax3.set_xlabel('time (s)')
    ax3.set_title('Comparison of Karma BIS items - Damage vs. Time')
    ax3.legend()

    ax4.plot(time_array, np.gradient(karma_dmg_blue_dcap_jg), label='BB Dcap JG')
    ax4.plot(time_array, np.gradient(karma_dmg_blue_ie_jg), label='BB IE JG')
    ax4.plot(time_array, np.gradient(karma_dmg_dcap_ie_jg), label='Dcap IE JG')
    ax4.plot(time_array, np.gradient(karma_dmg_blue_dcap_as), label='Blue Dcap AS')
    ax4.plot(time_array, np.gradient(karma_dmg_blue_jg_as), label='Blue JG AS')
    ax4.plot(time_array, np.gradient(karma_dmg_blue_hoj_as), label='Blue HOJ AS')
    ax4.set_xlabel('time (s)')
    ax4.set_title('Comparison of Karma BIS items - DPS vs. Time')
    ax4.legend()

    plt.xlim([0, 20])
    plt.ylim(ymin=0)
    plt.legend()
    plt.show()

# make_compare_mana()
make_compare_bis()