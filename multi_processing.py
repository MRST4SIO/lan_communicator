import multiprocessing
import time

def ciezkie_obliczenia(liczba):
  print(f"Liczę dla {liczba}...")

  wynik = 0
  for i in range(10**9):
    wynik += i * liczba
  return wynik


if __name__ == "__main__":
  liczby = [1, 2, 3, 4]

  start = time.perf_counter()
  with multiprocessing.Pool() as pool:
    wyniki = pool.map(ciezkie_obliczenia, liczby)
  koniec = time.perf_counter()

  print(f"Wyniki: {wyniki}")
  print(f"Czas wykonania: {koniec - start:.10f} sekundy")