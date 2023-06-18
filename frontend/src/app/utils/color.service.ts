import {Injectable} from '@angular/core';

@Injectable()
export class ColormapService {
  // Stores whether the direction for coloring is ASC (= true) or DESC (= false)
  // TODO: Continue
  colorMapDirection: Map<string, boolean> = new Map([
    ["distance", true], // higher = worse
    ["duration", true], // higher = worse
    ["efficiency", false], // higher = good
    ["catastrophy", true], // higher = worse
    ["co2", true], // high = worse
  ])

  getColor(score: number, minValue: number, maxValue: number, inverse: boolean = false): string {
    // Map the score value to the range [0, 1]
    let normalizedScore = (score - minValue) / (maxValue - minValue);
    if (inverse) normalizedScore = (1 - normalizedScore);
    const hue = (normalizedScore * (120 - 0)) + 0;
    return 'hsl(' + hue + ', 100%, 40%)';
  }

  generateColormap(objects: any[]): Map<string, string>[] {
    const colormaps: Map<string, string>[] = [];

    // Find the minimum and maximum values for each property
    const propertyMinMax: Map<string, { min: number, max: number }> = new Map();

    let obj: any;
    let key: any
    for (obj of objects) {
      for (key of Object.keys(obj)) {
        if (obj.hasOwnProperty(key)) {
          const value = obj[key];
          propertyMinMax.set(key, {
            min: Math.min(propertyMinMax.get(key)?.min || Infinity, value),
            max: Math.max(propertyMinMax.get(key)?.max || -Infinity, value),
          })
        }
      }
    }

    // Generate the colormap for each property
    for (obj of objects) {
      const colormap = new Map<string, string>();
      for (key of Object.keys(obj)) {
        const val = obj[key]
        if (isNaN(+val)) continue;
        const minValue = propertyMinMax.get(key)?.min || 0;
        const maxValue = propertyMinMax.get(key)?.max || 0;
        // TODO: Swap min max if we've found a true value in MapDirection
        const inverse = this.colorMapDirection.get(key) || false; // Check if the property should be inverse
        const color = this.getColor(val, minValue, maxValue, inverse);
        colormap.set(key, color);
      }
      colormaps.push(colormap);
    }

    return colormaps;
  }
}
