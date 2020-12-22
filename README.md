# Python Space Engineers Prometheus Exporter

[![PyPI](https://img.shields.io/pypi/v/se-exporter.svg)](https://pypi.org/project/se-exporter/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/se-exporter.svg)](https://pypi.org/project/space-engineers-exporter)
[![License: MIT](https://img.shields.io/badge/license-MIT-%23373737.svg)](htts://github.com/akimrx/space-engineers-exporters/LICENSE)

## Installing

* Installing with **pip**:
```bash
pip3 install se-exporter
```

* Installing from source:
```bash
git clone https://github.com/akimrx/space-engineers-exporter.git --recursive
cd space-engineers-exporter
make install  # or python3 setup.py install
```

## Usage

### Help output
```
Arguments:
  -h host, --host host                 Space Engineers Server (API) host
  -p port, --port port                 SE Remote API port. Default: 8080
  -t key, --token key                  SE Remote API secret key
  --listen-addr addr                   Address on which to expose metrics.
                                       Default: 0.0.0.0
  --listen-port port                   Port on which to expose metrics.
                                       Default: 9122
  --help                               Show this help message
  --version                            Show exporter version

Options:
  -c file, --config file               Path to the config file
  -a, --run-async                      Enable async collect metrics from SE.
                                       It works much faster. If your se server
                                       doesn't have good perfomance - don't
                                       use this feature
  --loglevel debug/info/warning/error  Log facility. Default: info
```

### Config example
```yaml
host: localhost
port: 5000

token: xY12qwe6ZZx123==
loglevel: info

listen_addr: 0.0.0.0
listen_port: 9122

run_async: true
```

### Examples

* Run with config file:
```bash
se-exporter --config-file /home/akimrx/config.yml
```

* Run with args:
```bash
se-exporter -h 0.0.0.0 -p 8080 --listen-port 9122 --token "XYZQWERty123-==" --run-async
```


## Exported metrics

Metric | Type | Labels | Description
-------|------|--------|------------
`players_count` | gauge | `server`, `world` | Total online players on the server
`player_ping` | gauge | `server`, `world`, `player_name`, `player_id`, `faction` | Player ping
`total_banned_players` | gauge | `server`, `world` | Total banned players on the server
`total_kicked_players` | gauge | `server`, `world` | Total kicked players on the server
`server_is_ready` | gauge | `server`, `world` | The server is ready to connect players
`simulation_speed` | gauge | `server`, `world` | Current world simulation speed
`simulation_cpu_load` | gauge | `server`, `world` | Current CPU load by simulation
`server_game_uptime_seconds` | gauge | `server`, `world` | Time during which the server is ready to play
`total_pcu_used` | gauge | `server`, `world` | Total used PCU on the ingame world by all
`pirate_total_pcu_used` | gauge | `server`, `world` | Total used PCU on the ingame world by pirates
`planets_count` | gauge | `server`, `world` | Number of planets on the game world
`total_grids` | gauge | `server`, `world` | Number of grids on the game world
`total_asteroids` | gauge | `server`, `world` | Number of asteroids on the game world
`total_floating_objects` | gauge | `server`, `world` | Number of floating objects on the game world
`characters_count` | gauge | `server`, `world` | Count of total characters on the game world

### Example real metrics output
```bash
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 246.0
python_gc_objects_collected_total{generation="1"} 222.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 82.0
python_gc_collections_total{generation="1"} 7.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="7",patchlevel="4",version="3.7.4"} 1.0
# HELP se_request_processing Time spent collecting SE server data
# TYPE se_request_processing summary
se_request_processing_count 1.0
se_request_processing_sum 0.903450259
# HELP se_request_processing_created Time spent collecting SE server data
# TYPE se_request_processing_created gauge
se_request_processing_created 1.6086711216817129e+09
# HELP players_count Number of online players on the server
# TYPE players_count gauge
players_count{server="se by akimrx",world="star system"} 1.0
# HELP server_is_ready The server is ready to connect players
# TYPE server_is_ready gauge
server_is_ready{server="se by akimrx",world="star system"} 1.0
# HELP player_ping Just players ping
# TYPE player_ping gauge
player_ping{faction="FLEX",player_id="12345678910111213",player_name="akimrx",server="se by akimrx",world="star system"} 13.0
player_ping{faction="FLEX",player_id="12345678910111214",player_name="rust",server="se by akimrx",world="star system"} 26.0
# HELP planets_count Number of planets in the game world
# TYPE planets_count gauge
planets_count{server="se by akimrx",world="star system"} 8.0
# HELP simulation_speed Current simulation speed in the game world
# TYPE simulation_speed gauge
simulation_speed{server="se by akimrx",world="star system"} 1.02
# HELP simulation_cpu_load CPU load generated by the simulation
# TYPE simulation_cpu_load gauge
simulation_cpu_load{server="se by akimrx",world="star system"} 21.0
# HELP server_game_uptime_seconds Time during which the server is ready to play
# TYPE server_game_uptime_seconds gauge
server_game_uptime_seconds{server="se by akimrx",world="star system"} 16529.0
# HELP total_pcu_used Number of total used PCU on the server
# TYPE total_pcu_used gauge
total_pcu_used{server="se by akimrx",world="star system"} 51902.0
# HELP pirate_total_pcu_used Number of total used PCU by Pirates on the server
# TYPE pirate_total_pcu_used gauge
pirate_total_pcu_used{server="se by akimrx",world="star system"} 3729.0
# HELP total_grids Count of total grids on the game world
# TYPE total_grids gauge
total_grids{server="se by akimrx",world="star system"} 14.0
# HELP total_asteroids Count of total asteroids on the game world
# TYPE total_asteroids gauge
total_asteroids{server="se by akimrx",world="star system"} 119.0
# HELP total_floating_objects Count of total floating objects on the game world
# TYPE total_floating_objects gauge
total_floating_objects{server="se by akimrx",world="star system"} 84.0
# HELP characters_count Count of total characters (including disconnected, but are on the server) on the game world
# TYPE characters_count gauge
characters_count{server="se by akimrx",world="star system"} 3.0
# HELP total_banned_players Count of total banned players on the game world
# TYPE total_banned_players gauge
total_banned_players{server="se by akimrx",world="star system"} 1.0
# HELP total_kicked_players Count of total kicked players on the game world
# TYPE total_kicked_players gauge
total_kicked_players{server="se by akimrx",world="star system"} 2.0
```