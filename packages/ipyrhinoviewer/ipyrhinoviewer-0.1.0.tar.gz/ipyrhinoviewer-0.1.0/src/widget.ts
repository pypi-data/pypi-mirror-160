// Copyright (c) Florian Jaeger
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';
import * as THREE from 'three';
import { MODULE_NAME, MODULE_VERSION } from './version';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Rhino3dmLoader } from 'three/examples/jsm/loaders/3DMLoader';

// Import the CSS
import '../css/widget.css';

export class RhinoModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: RhinoModel.model_name,
      _model_module: RhinoModel.model_module,
      _model_module_version: RhinoModel.model_module_version,
      _view_name: RhinoModel.view_name,
      _view_module: RhinoModel.view_module,
      _view_module_version: RhinoModel.view_module_version,
      value: '',
      height: 700,
      width: 1000,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'RhinoModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'RhinoView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

function load3dmModel(
  scene: THREE.Scene,
  filePath: string,
  options: { receiveShadow: any; castShadow: any }
) {
  const { receiveShadow, castShadow } = options;
  return new Promise((resolve, reject) => {
    const loader = new Rhino3dmLoader();
    loader.setLibraryPath('https://cdn.jsdelivr.net/npm/rhino3dm@0.15.0-beta/');
    loader.load(
      filePath,
      (data: any) => {
        const obj = data;
        obj.position.y = 0;
        obj.position.x = 0;
        obj.receiveShadow = receiveShadow;
        obj.castShadow = castShadow;
        scene.add(obj);

        obj.traverse((child: any) => {
          if (child.isObject3D) {
            child.castShadow = castShadow;
            child.receiveShadow = receiveShadow;
          }
        });

        resolve(obj);
      },
      undefined,
      (error: any) => {
        console.log(error);
        reject(error);
      }
    );
  });
}

export class RhinoView extends DOMWidgetView {
  private path = this.model.get('value');
  private width = this.model.get('width');
  private height = this.model.get('height');

  render() {
    const error = document.createElement('p');
    if (this.width < 100 || this.width > 3000) {
      error.textContent = 'Width must be in range of 100-3000';
      this.el.appendChild(error);
      return;
    }
    if (this.height < 100 || this.height > 3000) {
      error.textContent = 'Height must be in range of 100-3000';
      this.el.appendChild(error);
      return;
    }
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      this.width / this.height,
      0.1,
      1000
    );

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(this.width, this.height);
    const ambientLight = new THREE.AmbientLight(0xcccccc, 2);
    scene.add(ambientLight);
    const controls = new OrbitControls(camera, renderer.domElement);
    const onContextMenu = (event: Event) => {
      event.stopPropagation();
    };
    this.el.addEventListener('contextmenu', onContextMenu);
    load3dmModel(scene, '/tree/' + this.path, {
      receiveShadow: true,
      castShadow: false,
    })
      .then(() => {
        this.el.appendChild(renderer.domElement);
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
        animate();
      })
      .catch(() => {
        error.textContent =
          'Error: ' + this.model.get('value') + ' was not found';
        this.el.appendChild(error);
        return;
      });

    camera.position.z = 5;

    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }

    animate();
  }

  value_changed(): void {
    this.path = this.model.get('value');
  }
}
