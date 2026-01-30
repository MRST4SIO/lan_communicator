import asyncio

async def zaparz_kawe():
    print("Zaczynam parzyć kawę...")
    await asyncio.sleep(3)  # NIE blokujemy całego programu, tylko tę funkcję
    print("Kawa gotowa!")
    return "Ciepła Latte"

async def smaz_jajka():
    print("Zaczynam smażyć jajka...")
    await asyncio.sleep(2)
    print("Jajka gotowe!")
    return "Jajecznica"

async def main():
    print("---Start---")

    wyniki = await asyncio.gather(smaz_jajka(), zaparz_kawe())
    print(f"Zjedzono: {wyniki}")
    print("---Koniec sniadania---")

asyncio.run(main())