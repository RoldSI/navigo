import {Injectable} from '@angular/core';

@Injectable()
export class ColormapService {
  getColor(score: number, minValue: number, maxValue: number): string {
    // Map the score value to the range [0, 1]
    const normalizedScore = (score - minValue) / (maxValue - minValue);

    // Convert the normalized score to the corresponding hue value
    const hue = (1 - normalizedScore) * 120; // 120 corresponds to the range of hues from red to green

    // Adjust saturation and lightness for darker and richer colors
    const saturation = 100; // Keep full saturation
    const lightness = 30 + normalizedScore * 40; // Range of lightness: 30% to 70%

    // Create an HSL color string with adjusted saturation and lightness
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
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

          // if (!propertyMinMax.hasOwnProperty(key)) {
          //   propertyMinMax.set(key, {min: Infinity, max: -Infinity});
          // }

          propertyMinMax.set(key, {
            min: Math.min(propertyMinMax.get(key)?.min || Infinity, value),
            max: Math.max(propertyMinMax.get(key)?.max || -Infinity, value),
          })
        }
      }
    }

    // Generate the colormap for each property
    for (obj of objects) {
      console.log(obj);
      const colormap = new Map<string, string>();
      for (key of Object.keys(obj)) {
        const val = obj[key]
        console.log(val, " and ", isNaN(+val));
        if (isNaN(+val)) continue;
        const minValue = propertyMinMax.get(key)?.min || 0;
        const maxValue = propertyMinMax.get(key)?.max || 0;
        const color = this.getColor(val, minValue, maxValue);
        colormap.set(key, color);
      }
      colormaps.push(colormap);
    }

    return colormaps;
  }
}
