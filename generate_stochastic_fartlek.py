from random import choice
from statistics import median


def get_fc_thresh(time: int, time_array: range) -> int:
    """genera la frequenza cardiaca relativa a cui lavorare dato un certo intervallo

    Args:
        time (int): durata in minuti dell'intervallo
        time_array (range): range delle durate degli intervalli in minuti

    Returns:
        int: frequenza relativa (moltiplicata per 100)
    """
    if time > median(time_array):
        return 70
    else:
        return 85


def print_interval_infos(
    high_intensity_time: int, recovery_time: int, time_array: range
) -> None:
    """stampa le informazioni relative all'intervallo intenso e a quello di recupero

    Args:
        high_intensity_time (int): durata in minuti dell'intervallo intenso
        recovery_time (int): urata in minuti del recupero attivo
        time_array (range, optional): range delle durate degli intervalli in minuti
    """
    high_intensity_rfreq = get_fc_thresh(high_intensity_time, time_array)
    print(
        f"{high_intensity_time}min {high_intensity_rfreq}% freq max",
        f"{recovery_time}min recupero attivo",
        sep="\n",
        end="\n",
    )


def generate_fartlek(
    total_time: int, time_array: range, recovery_modifiers: int
) -> None:
    """stampa l'allenamento

    Args:
        total_time (int): tempo totale di allenamento
        time_array (range, optional): range delle durate degli intervalli in minuti
        recovery_modifiers (int): moltiplicatore dei tempi di recupero, [1,3] equivalente di livello [avanzato, intermedio, principiante]
    """
    print("20m riscaldamento")
    while total_time > 0:
        if total_time > 10:
            high_intensity_time = choice(time_array)
            recovery_range = range(high_intensity_time, max(time_array) + 1)
            recovery_time = choice(recovery_range) * recovery_modifiers
            total_time -= high_intensity_time + recovery_time
            print_interval_infos(high_intensity_time, recovery_time, time_array)
        elif total_time > 1:
            total_activity_quota = recovery_modifiers + 1
            high_intensity_time = int(total_time / total_activity_quota)
            recovery_time = total_time - high_intensity_time
            total_time -= high_intensity_time + recovery_time

    print("10min defaticamento")


if __name__ == "__main__":
    standard_mintime = 2
    standard_maxtime = 5

    total_time = 0

    while total_time == 0:
        total_time_input = int(
            input(
                "tempo allenamento in minuti (escluso tempo di riscaldamento e defaticamento): "  # noqa
            )
        )
        if total_time_input < 10:
            print("sotto i 10 minuti attivi non ha senso")  # noqa
        else:
            total_time = total_time_input

    recovery_modifiers = 0

    while recovery_modifiers == 0:
        recovery_modifiers_input = int(
            input(
                "inserire moltiplicatore dei tempi di recupero [1,3], equivalente di livello [avanzato, intermedio, principiante]: "  # noqa
            )
        )
        if recovery_modifiers_input in range(1, 4):
            recovery_modifiers = recovery_modifiers_input
        else:
            print("scegliere tra 1 e 3")  # noqa

    modifiers = 4
    while modifiers == 4:
        modifiers_input = int(
            input("inserire variazione di difficoltà [-1,+2]: ")
        )  # noqa
        if modifiers_input in range(-1, 3):
            modifiers = modifiers_input
        else:
            print("inserire una variazione compresa tra -1 e 2")

    time_array = range(standard_mintime + modifiers, standard_maxtime + modifiers)

    generate_fartlek(total_time, time_array, recovery_modifiers)
