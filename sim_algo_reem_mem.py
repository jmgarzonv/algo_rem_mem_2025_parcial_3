#!/usr/bin/env python

# marcos_libres = [0x0,0x1,0x2]
# reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
# segmentos =[ ('.text', 0x00, 0x1A),
#              ('.data', 0x40, 0x28),
#              ('.heap', 0x80, 0x1F),
#              ('.stack', 0xC0, 0x22),
#             ]

def procesar(segmentos, reqs, marcos_libres):
    page_table = {}  # página lógica -> marco físico
    lru_tracker = {}  # página lógica -> timestamp de último uso
    results = []
    current_time = 0  # contador de accesos

    def direccion_valida(req):
        for nombre, base, limite in segmentos:
            if base <= req < base + limite:
                return True
        return False

    for req in reqs:
        if not direccion_valida(req):
            results.append((req, 0x1FF, "Segmentation Fault"))
            continue

        pagina_logica = req // 16
        offset = req % 16

        if pagina_logica in page_table:
            marco = page_table[pagina_logica]
            lru_tracker[pagina_logica] = current_time
            results.append((req, (marco << 4) | offset, "Marco ya estaba asignado"))
        else:
            if marcos_libres:
                marco = marcos_libres.pop()
                page_table[pagina_logica] = marco
                lru_tracker[pagina_logica] = current_time
                results.append((req, (marco << 4) | offset, "Marco libre asignado"))
            else:
                pagina_reemplazo = min(lru_tracker, key=lru_tracker.get)
                marco = page_table[pagina_reemplazo]

                del page_table[pagina_reemplazo]
                del lru_tracker[pagina_reemplazo]

                page_table[pagina_logica] = marco
                lru_tracker[pagina_logica] = current_time
                results.append((req, (marco << 4) | offset, "Marco asignado"))

        current_time += 1

    return results


    
def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    marcos_libres = [0x0,0x1,0x2]
    reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
    segmentos =[ ('.text', 0x00, 0x1A),
                ('.data', 0x40, 0x28),
                ('.heap', 0x80, 0x1F),
                ('.stack', 0xC0, 0x22),
                ]



    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)

