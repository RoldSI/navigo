import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'distanceFormat'
})
export class DistanceFormatPipe implements PipeTransform {
  transform(value: number | string): string {
    if (isNaN(+value)) return value + "";
    else value = Number(value);

    if (value >= 1000) {
      const kmValue = (value / 1000).toFixed(2);
      return `${kmValue}`;
    } else {
      return `${value.toFixed(2)}`;
    }
  }
}

@Pipe({
  name: 'timeFormat'
})
export class TimeFormatPipe implements PipeTransform {
  transform(value: number | string): string {
    if (isNaN(+value)) return value + "";
    else value = Number(value);

    if (value >= 86400) {
      const daysValue = (value / 86400).toFixed(2);
      return `${daysValue}`;
    } else if (value >= 3600) {
      const hoursValue = (value / 3600).toFixed(2);
      return `${hoursValue}`;
    } else if (value >= 60) {
      const minutesValue = (value / 60).toFixed(2);
      return `${minutesValue}`;
    } else {
      return `${value.toFixed(2)}`;
    }
  }
}

@Pipe({
  name: 'distanceUnit'
})
export class DistanceUnitPipe implements PipeTransform {
  transform(value: number | string): string {
    if (isNaN(+value)) return value + "";
    else value = Number(value);

    if (value >= 1000) {
      return `km`;
    } else {
      return `m`;
    }
  }
}

@Pipe({
  name: 'co2Format'
})
export class Co2Pipe implements PipeTransform {
  transform(value: number | string): string {
    if (isNaN(+value)) return value + "";
    else value = Number(value);

    if (value >= 1000) {
      const kgValue = value / 1000;
      return kgValue.toFixed(2);
    } else {
      return value.toFixed(2);
    }
  }
}

@Pipe({
  name: 'co2Unit'
})
export class Co2UnitPipe implements PipeTransform {
  transform(value: number | string): string {
    const prefix = " CO2"
    if (isNaN(+value)) return value + prefix;
    else value = Number(value);
    return (value >= 1000 ? 'kg' : 'g') + prefix;
  }
}

@Pipe({
  name: 'roundToTwoDecimals'
})
export class RoundToTwoDecimalsPipe implements PipeTransform {
  transform(value: number | string): number | string {
    if (isNaN(+value)) return value + "";
    else value = Number(value);
    return Math.round(value * 100) / 100; // Round to two decimal places
  }
}

@Pipe({
  name: 'timeUnit'
})
export class TimeUnitPipe implements PipeTransform {
  transform(value: number | string): string {
    if (isNaN(+value)) return value + "";
    else value = Number(value);

    if (value >= 86400) {
      return `Days`;
    } else if (value >= 3600) {
      return `Hours`;
    } else if (value >= 60) {
      return `Minutes`;
    } else {
      return `Seconds`;
    }
  }
}
