import { Circle, CubicHorizontal, subStyleProps, Rect, Graph, ExtensionCategory } from '@antv/g6';
import { text } from 'body-parser';

export class breathNode extends Circle {
    onCreate() {
        const halo = this.shapeMap.halo;
        halo.animate([{ lineWidth: 0 }, { lineWidth: 20 }], {
            duration: 1000,
            iterations: Infinity,
            direction: 'alternate',
        });
    }

    getSubtitleStyle(attributes) {
        return {
            x: 0,
            y: 45, // 放在主标题下方
            text: attributes.subtitle || '',
            fontSize: 12,
            fill: '#666',
            textAlign: 'center',
            textBaseline: 'middle',
        };
    }

    // 绘制副标题
    drawSubtitleShape(attributes, container) {
        const subtitleStyle = this.getSubtitleStyle(attributes);
        this.upsert('subtitle', 'text', subtitleStyle, container);
    }
    render(cfg, group) {
        super.render(cfg, group);
        // 绘制副标题
        this.drawSubtitleShape(cfg, group);
    }
  
}

export class FlyMarkerCubic extends CubicHorizontal {

  getMarkerStyle(attributes) {
    return { r: 1, fill: '#c3d5f9', labelText: "飞机", offsetPath: this.shapeMap.key, ...subStyleProps(attributes, 'marker') };
  }

  onCreate() {
    console.log('onCreate', this.getMarkerStyle(this.attributes));
    const marker = this.upsert('marker', Circle, this.getMarkerStyle(this.attributes), this);
    marker.animate(
    [
        { offsetDistance: 0 }, 
        { offsetDistance: 1 }
    ], {
      duration: 3000,
      iterations: Infinity,
    });
  }
}
