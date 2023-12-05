MapGenName = "MADAFAGA"
Heightmap = "0 0 0 0 0"
Size = (256, 256)
FluidHeightmap = " ".join(["0"] * (Size[0] * Size[1]))
FluidDirectionmap = " ".join(["0:0:0:0"] * (Size[0] * Size[1]))

json = (f'''{{
  "GameVersion":"0.5.3.2-3a67edf-xsw",
  "MadeWith": "{MapGenName}",
  "Timestamp":"INSERT CREATION TIME",
  "Singletons":{{
    "MapSize":{{
      "Size":{{
        "X":{Size[0]},
        "Y":{Size[1]}
      }}
    }},
    "TerrainMap":{{
      "Heights":{{
        "Array":"{Heightmap}"
      }}
    }},
    "CameraStateRestorer":{{
      "SavedCameraState":{{
        "Target":{{
          "X":0.0,
          "Y":0.0,
          "Z":0.0
        }},
        "ZoomLevel":0.0,
        "HorizontalAngle":30.0,
        "VerticalAngle":70.0
      }}
    }},
    "WaterMap":{{
      "WaterDepths":{{
        "Array":"{FluidHeightmap}"
      }},
      "Outflows":{{
        "Array":"{FluidDirectionmap}"
      }}
    }},
    "ContaminationMap":{{
      "Contaminations":{{
        "Array":"{FluidHeightmap}"
      }}
    }},
    "HazardousWeatherHistory":{{
      "History":[]
    }},
    "MapThumbnailCameraMover":{{
      "CurrentConfiguration":{{
        "Position":{{
          "X":128.0,
          "Y":164.553619,
          "Z":-68.10739
        }},
        "Rotation":{{
          "X":0.342020124,
          "Y":0.0,
          "Z":0.0,
          "W":0.9396926
        }},
        "ShadowDistance":150.0
      }}
    }}
  }},
  "Entities":[]
}}''')

print(json)
