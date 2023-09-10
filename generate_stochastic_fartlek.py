from random import choice
from statistics import median
from typing import Callable, no_type_check


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


def seconds_to_minutes(time: int) -> str:
    """ritorna il tempo in un formato che comprende minuti e secondi (quando i secondi superano i 60)

    Args:
        time (int): tempo

    Returns:
        str: formato %m%s
    """
    if time > 60:
        return f"{time//60}m{time%60}s"

    else:
        return f"{time}s"


@no_type_check
def generate_training_session(f: Callable[[list[int | range]], None]) -> None:
    """decoratore che stampa per ogni tipologia di allenamento 20 minuti di riscaldamento e 10 di defaticamento

    Args:
        f (Callable[[list[int | range]], None]): funzione del tipo di allenamento scelto
    """

    def wrapper(*args, **kwargs):
        print("20m riscaldamento")
        f(*args, **kwargs)
        print("10min defaticamento")

    return wrapper


@generate_training_session
def generate_fartlek(
    total_time: int, time_array: range, recovery_modifiers: int
) -> None:
    """stampa l'allenamento

    Args:
        total_time (int): tempo totale di allenamento
        time_array (range, optional): range delle durate degli intervalli in minuti
        recovery_modifiers (int): moltiplicatore dei tempi di recupero, [1,3] equivalente di livello [avanzato, intermedio, principiante]
    """
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
            break


def generate_interval_times(type: str) -> list[int]:
    """genera i tempi di attività/riposo in base al tipo di intensità scelta

    Args:
        type (str): il tipo di intensità scelta

    Returns:
        tuple[int]: durata totale dell'intervallo, tempo di attività, tempo di recupero
    """
    if type == "m":
        active_duration = range(75, 91)
        interval_time = 120
    else:
        active_duration = range(67, 84)
        interval_time = 60

    active_freq = choice(active_duration)
    activity_time = int(interval_time * active_freq / 100)
    rest_time = interval_time - activity_time

    return [interval_time, activity_time, rest_time]


@generate_training_session
def hiit_timings(total_time: int) -> None:
    """genera un programma di allenamento di tipo hiit

    Args:
        total_time (int): tempo totale di allenamento
    """
    total_time = total_time * 60
    consecutive_hi_count = 0
    effective_training_time = 0

    while total_time > 0:
        if effective_training_time >= 900:
            print("1m rest opzionale")
            effective_training_time = 0
        if total_time > 120:
            random_intensity_choice = choice(["m", "h"])
            if consecutive_hi_count == 4:
                consecutive_hi_count = 0
                print("30s di recupero attivo o rest", sep="\n")
                total_time -= 30
            else:
                interval_time, activity_time, rest_time = generate_interval_times(
                    random_intensity_choice
                )
                total_time -= interval_time
                effective_training_time += interval_time
                if random_intensity_choice == "h":
                    consecutive_hi_count += 1
                    print(
                        f"{activity_time}s ad alta intensità",
                        f"{rest_time}s di recupero attivo",
                        sep="\n",
                    )
                else:
                    consecutive_hi_count = 0
                    print(
                        f"{seconds_to_minutes(activity_time)} a media intensità",
                        f"{rest_time}s di recupero attivo",
                        sep="\n",
                    )
        else:
            print(f"{seconds_to_minutes(total_time)} a media intensità", sep="\n")
            break


def main() -> None:
    while "training_type" not in locals():
        try:
            training_type_input = int(
                input("scegliere tipo allenamento fartlek [1], hiit [2]: ")
            )
            if training_type_input in [1, 2]:
                training_type = training_type_input
            else:
                print("scegliere 1 o 2")
        except ValueError:
            print("""l'input deve essere un numero""")

    while "total_time" not in locals():
        try:
            total_time_input = int(
                input(
                    "tempo allenamento in minuti (escluso tempo di riscaldamento e defaticamento): "
                )
            )
            if total_time_input < 10:
                print("sotto i 10 minuti attivi non ha senso")
            else:
                total_time = total_time_input
        except ValueError:
            print("""l'input deve essere un numero""")

    if training_type == 1:
        standard_mintime = 2
        standard_maxtime = 5

        while "recovery_modifiers" not in locals():
            try:
                recovery_modifiers_input = int(
                    input(
                        "inserire moltiplicatore dei tempi di recupero [1,3], equivalente di livello [avanzato, intermedio, principiante]: "
                    )
                )
                if recovery_modifiers_input in range(1, 4):
                    recovery_modifiers = recovery_modifiers_input
                else:
                    print("scegliere tra 1 e 3")
            except ValueError:
                print("""l'input deve essere un numero""")

        while "modifiers" not in locals():
            try:
                modifiers_input = int(
                    input("inserire variazione di difficoltà [-1,+2]: ")
                )
                if modifiers_input in range(-1, 3):
                    modifiers = modifiers_input
                else:
                    print("inserire una variazione compresa tra -1 e 2")
            except ValueError:
                print("""l'input deve essere un numero""")

        time_array = range(standard_mintime + modifiers, standard_maxtime + modifiers)
        generate_fartlek(total_time, time_array, recovery_modifiers)

    if training_type == 2:
        hiit_timings(total_time)


if __name__ == "__main__":
    main()
