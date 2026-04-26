from collections import defaultdict
import importlib


def normalize(ext: str) -> str:
   ext = ext.lower().strip()
   for prefix in ["rv32_", "rv64_", "rv_"]:
      if ext.startswith(prefix):
         ext = ext[len(prefix):]
   return ext


def build_extension_graph() -> dict[str, set[str]]:
   requests = importlib.import_module("requests")
   url = "https://raw.githubusercontent.com/rpsene/riscv-extensions-landscape/main/src/instr_dict.json"
   data = requests.get(url, timeout=20).json()

   graph: dict[str, set[str]] = defaultdict(set)

   for _, info in data.items():
      tags = info.get("extension", [])
      if isinstance(tags, str):
         tags = [tags]

      normalized = [normalize(tag) for tag in tags]

      for i, src in enumerate(normalized):
         for dst in normalized[i + 1 :]:
            graph[src].add(dst)
            graph[dst].add(src)

   return graph


def draw_extension_graph() -> None:
   nx = importlib.import_module("networkx")
   plt = importlib.import_module("matplotlib.pyplot")

   graph = build_extension_graph()
   g = nx.Graph()

   for ext, neighbors in graph.items():
      for neighbor in neighbors:
         g.add_edge(ext, neighbor)

   nx.draw(g, with_labels=True)
   plt.show()


if __name__ == "__main__":
   draw_extension_graph()