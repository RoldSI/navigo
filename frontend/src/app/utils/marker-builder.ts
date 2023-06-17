import SymbolPath = google.maps.SymbolPath;


export enum MarkerType {
  End,
  Default,
  Favorite,
  Information
}

export class MarkerBuilder {
  private markerOptions: google.maps.MarkerOptions = {};

  private markerSymbolMap: Map<MarkerType, string> = new Map([
    [MarkerType.Information, "M112.02,0C64.877,0,26.524,38.354,26.524,85.496c0,32.207,17.907,60.301,44.281,74.876l37.589,61.199\n" +
    "\tc0.963,1.569,2.46,2.469,4.106,2.469c1.659,0,3.171-0.912,4.146-2.501l38.131-62.054c25.523-14.807,42.739-42.417,42.739-73.989\n" +
    "\tC197.516,38.354,159.163,0,112.02,0z M124.687,138.729h-24v-66h24V138.729z M112.933,62.587c-7.851,0-14.215-6.364-14.215-14.215\n" +
    "\tc0-7.851,6.364-14.215,14.215-14.215s14.215,6.365,14.215,14.215C127.148,56.223,120.784,62.587,112.933,62.587z"],
    [MarkerType.Default,
      "M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z"],
    [MarkerType.Favorite, "m56,237 74-228 74,228L10,96h240"],
    [MarkerType.End, "M389.183,10.118c-3.536-2.215-7.963-2.455-11.718-0.634l-50.653,24.559c-35.906,17.409-77.917,16.884-113.377-1.418\n" +
    "\tc-38.094-19.662-83.542-18.72-120.789,2.487V20c0-11.046-8.954-20-20-20s-20,8.954-20,20v407.514c0,11.046,8.954,20,20,20\n" +
    "\ts20-8.954,20-20V220.861c37.246-21.207,82.694-22.148,120.789-2.487c35.46,18.302,77.47,18.827,113.377,1.418l56.059-27.18\n" +
    "\tc7.336-3.557,11.995-10.993,11.995-19.146V20.385C394.866,16.212,392.719,12.333,389.183,10.118z"]
  ]);


  setPosition(lat: number, lng: number): MarkerBuilder
  setPosition(pos: { lat: number, lng: number }): MarkerBuilder
  setPosition(arg1: number | { lat: number, lng: number }, lng?: number): MarkerBuilder {
    if (typeof arg1 === 'number' && typeof lng === 'number') {
      this.markerOptions.position = {
        lat: arg1,
        lng: lng
      };
    } else if (typeof arg1 === 'object') {
      this.markerOptions.position = arg1;
    }
    return this;
  }

  private setIconSymbol(path: SymbolPath | string, opts: {
                          fillColor?: string
                          fillOpacity?: number,
                          rotation?: number,
                          scale?: number,
                          strokeColor?: string,
                          strokeOpacity?: number,
                          strokeWeight?: number,
                          anchor?: {
                            x: number,
                            y: number
                          }
                        }
  ): MarkerBuilder {
    this.markerOptions.icon = {
      path: path,
      ...opts
    } as google.maps.Symbol;
    return this;
  }

  setZIndex(index: number): MarkerBuilder {
    this.markerOptions.zIndex = index;
    return this;
  }

  setDefaultIconSymbol(type: MarkerType): MarkerBuilder {
    const symbolPath = this.markerSymbolMap.get(type);
    if (!symbolPath) {
      console.warn("Symbol Path for Symbol Type ", type, " was not found!");
      return this;
    }
    switch (type) {
      case MarkerType.Default:
        // Set Z-Index
        this.setZIndex(100);
        // Default marker
        this.setIconSymbol(symbolPath, {
          fillColor: "#A01441",
          scale: .075,
          fillOpacity: 1,
          strokeColor: "#A01441",
          strokeOpacity: 1,
          strokeWeight: 2,
          anchor: {
            x: 200,
            y: 500
          }
        })
        break;
      case MarkerType.End:
        // Set Z-Index
        this.setZIndex(100);
        // Default marker
        this.setIconSymbol(symbolPath, {
          fillColor: "#A01441",
          scale: .075,
          fillOpacity: 1,
          strokeColor: "#A01441",
          strokeOpacity: 1,
          strokeWeight: 2,
          anchor: {
            x: 120,
            y: 450
          }
        })
        break;
      case MarkerType.Favorite:
        // Set Z-Index
        this.setZIndex(50);
        // Star marker for favorites
        this.setIconSymbol(symbolPath, {
          fillColor: "cyan",
          scale: .15,
          fillOpacity: 1,
          strokeColor: "cyan",
          strokeOpacity: 1,
          strokeWeight: 2,
          anchor: {
            x: 125,
            y: 250
          }
        })
        break;
      case MarkerType.Information:
        // Set Z-Index
        this.setZIndex(25);
        // Information marker
        this.setIconSymbol(symbolPath, {
          fillColor: "darkblue",
          scale: .15,
          fillOpacity: 1,
          strokeColor: "darkblue",
          strokeOpacity: 1,
          strokeWeight: 2,
          anchor: {
            x: 110,
            y: 225
          }
        })
        break;
      default:
        break;
    }
    return this;
  }

  buildMarker(): google.maps.MarkerOptions {
    return this.markerOptions;
  }
}
