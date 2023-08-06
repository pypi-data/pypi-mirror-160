/*! For license information please see 31a2278c.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[16117],{89194:(e,t,i)=>{i(48175),i(65660),i(70019);var r=i(9672),o=i(50856);(0,r.k)({_template:o.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},63864:(e,t,i)=>{i.d(t,{I:()=>r});const r=(e,t,i,r)=>{const[o,s,n]=e.split(".",3);return Number(o)>t||Number(o)===t&&(void 0===r?Number(s)>=i:Number(s)>i)||void 0!==r&&Number(o)===t&&Number(s)===i&&Number(n)>=r}},41682:(e,t,i)=>{i.d(t,{rY:()=>o,js:()=>s,yz:()=>a,yd:()=>l});var r=i(63864);const o=e=>e.data,s=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e,n=new Set([502,503,504]),a=e=>!!(e&&e.status_code&&n.has(e.status_code))||!(!e||!e.message||!e.message.includes("ERR_CONNECTION_CLOSED")&&!e.message.includes("ERR_CONNECTION_RESET")),l=async(e,t)=>(0,r.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:`/${t}/stats`,method:"get"}):o(await e.callApi("GET",`hassio/${t}/stats`))},69810:(e,t,i)=>{i.d(t,{lC:()=>s,CP:()=>n,Lm:()=>a,NC:()=>l,jP:()=>c});var r=i(63864),o=i(41682);const s=async e=>{(0,r.I)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:"/supervisor/reload",method:"post"}):await e.callApi("POST","hassio/supervisor/reload")},n=async e=>(0,r.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/supervisor/info",method:"get"}):(0,o.rY)(await e.callApi("GET","hassio/supervisor/info")),a=async e=>(0,r.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/info",method:"get"}):(0,o.rY)(await e.callApi("GET","hassio/info")),l=async(e,t)=>e.callApi("GET",`hassio/${t.includes("_")?`addons/${t}`:t}/logs`),c=async(e,t)=>{(0,r.I)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:"/supervisor/options",method:"post",data:t}):await e.callApi("POST","hassio/supervisor/options",t)}},43955:(e,t,i)=>{i.r(t);i(44577);var r=i(37500),o=i(33310),s=i(14516),n=i(7323),a=(i(9381),i(12373),i(81545),i(22098),i(2130),i(41682)),l=i(69810),c=i(24833),d=i(26765);i(60010),i(95306);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var s="static"===o?e:i;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!f(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,s=o.length-1;s>=0;s--){var n=t[e.placement];n.splice(n.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var n=0;n<e.length-1;n++)for(var a=n+1;a<e.length;a++)if(e[n].key===e[a].key&&e[n].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[n].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=v(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function h(e){var t,i=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function g(e,t,i){return g="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}},g(e,t,i||e)}function w(e){return w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},w(e)}!function(e,t,i,r){var o=p();if(r)for(var s=0;s<r.length;s++)o=r[s](o);var n=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var o,s=e[r];if("method"===s.kind&&(o=t.find(i)))if(m(s.descriptor)||m(o.descriptor)){if(f(s)||f(o))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");o.descriptor=s.descriptor}else{if(f(s)){if(f(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");o.decorators=s.decorators}u(s,o)}else t.push(s)}return t}(n.d.map(h)),e);o.initializeClassElements(n.F,a.elements),o.runClassFinishers(n.F,a.finishers)}([(0,o.Mo)("ha-config-section-updates")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_showSkipped",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_supervisorInfo",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){g(w(i.prototype),"firstUpdated",this).call(this,e),(0,n.p)(this.hass,"hassio")&&(0,l.CP)(this.hass).then((e=>{this._supervisorInfo=e}))}},{kind:"method",key:"render",value:function(){var e,t;const i=this._filterUpdateEntitiesWithInstall(this.hass.states,this._showSkipped);return r.dy`
      <hass-subpage
        back-path="/config/system"
        .hass=${this.hass}
        .narrow=${this.narrow}
        .header=${this.hass.localize("ui.panel.config.updates.caption")}
      >
        <div slot="toolbar-icon">
          <ha-icon-button
            .label=${this.hass.localize("ui.panel.config.updates.check_updates")}
            .path=${"M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"}
            @click=${this._checkUpdates}
          ></ha-icon-button>
          <ha-button-menu corner="BOTTOM_START" @action=${this._handleAction}>
            <ha-icon-button
              slot="trigger"
              .label=${this.hass.localize("ui.common.menu")}
              .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
            ></ha-icon-button>
            <mwc-list-item id="skipped">
              ${this._showSkipped?this.hass.localize("ui.panel.config.updates.hide_skipped"):this.hass.localize("ui.panel.config.updates.show_skipped")}
            </mwc-list-item>
            ${"dev"!==(null===(e=this._supervisorInfo)||void 0===e?void 0:e.channel)?r.dy`
                  <mwc-list-item id="beta">
                    ${"stable"===(null===(t=this._supervisorInfo)||void 0===t?void 0:t.channel)?this.hass.localize("ui.panel.config.updates.join_beta"):this.hass.localize("ui.panel.config.updates.leave_beta")}
                  </mwc-list-item>
                `:""}
          </ha-button-menu>
        </div>
        <div class="content">
          <ha-card outlined>
            <div class="card-content">
              ${i.length?r.dy`
                    <ha-config-updates
                      .hass=${this.hass}
                      .narrow=${this.narrow}
                      .updateEntities=${i}
                      showAll
                    ></ha-config-updates>
                  `:r.dy`
                    <div class="no-updates">
                      ${this.hass.localize("ui.panel.config.updates.no_updates")}
                    </div>
                  `}
            </div>
          </ha-card>
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"_handleAction",value:function(e){switch(e.detail.index){case 0:this._showSkipped=!this._showSkipped;break;case 1:this._toggleBeta()}}},{kind:"method",key:"_toggleBeta",value:async function(){if("stable"===this._supervisorInfo.channel){if(!await(0,d.g7)(this,{title:this.hass.localize("ui.dialogs.join_beta_channel.title"),text:r.dy`${this.hass.localize("ui.dialogs.join_beta_channel.warning")}
          <br />
          <b> ${this.hass.localize("ui.dialogs.join_beta_channel.backup")} </b>
          <br /><br />
          ${this.hass.localize("ui.dialogs.join_beta_channel.release_items")}
          <ul>
            <li>Home Assistant Core</li>
            <li>Home Assistant Supervisor</li>
            <li>Home Assistant Operating System</li>
          </ul>
          <br />
          ${this.hass.localize("ui.dialogs.join_beta_channel.confirm")}`,confirmText:this.hass.localize("ui.panel.config.updates.join_beta"),dismissText:this.hass.localize("ui.common.cancel")}))return}try{const e={channel:"stable"===this._supervisorInfo.channel?"beta":"stable"};await(0,l.jP)(this.hass,e),await(0,l.lC)(this.hass)}catch(e){(0,d.Ys)(this,{text:(0,a.js)(e)})}}},{kind:"method",key:"_checkUpdates",value:async function(){(0,c.M$)(this,this.hass)}},{kind:"field",key:"_filterUpdateEntitiesWithInstall",value:()=>(0,s.Z)(((e,t)=>(0,c.Fj)(e,t)))},{kind:"field",static:!0,key:"styles",value:()=>r.iv`
    .content {
      padding: 28px 20px 0;
      max-width: 1040px;
      margin: 0 auto;
    }
    ha-card {
      max-width: 600px;
      margin: 0 auto;
      height: 100%;
      justify-content: space-between;
      flex-direction: column;
      display: flex;
      margin-bottom: max(24px, env(safe-area-inset-bottom));
    }

    .card-content {
      display: flex;
      justify-content: space-between;
      flex-direction: column;
      padding: 0;
    }

    .no-updates {
      padding: 16px;
    }
  `}]}}),r.oi)}}]);
//# sourceMappingURL=31a2278c.js.map