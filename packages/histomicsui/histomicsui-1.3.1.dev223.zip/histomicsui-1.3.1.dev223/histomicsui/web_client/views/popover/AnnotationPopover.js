import _ from 'underscore';
import $ from 'jquery';

import { restRequest } from '@girder/core/rest';
import ElementCollection from '@girder/large_image_annotation/collections/ElementCollection';
import convertRectangle from '@girder/large_image_annotation/annotations/geometry/rectangle';
import convertEllipse from '@girder/large_image_annotation/annotations/geometry/ellipse';
import convertCircle from '@girder/large_image_annotation/annotations/geometry/circle';
import convert from '@girder/large_image_annotation/annotations/convert';

import events from '../../events';
import View from '../View';
import annotationPopover from '../../templates/popover/annotationPopover.pug';
import '../../stylesheets/popover/annotationPopover.styl';

/**
 * Format a point as a string for the user.
 */
function point(p) {
    return `(${parseInt(p[0])}, ${parseInt(p[1])})`;
}

/**
 * Format a distance as a string for the user.
 */
function length(p, scale) {
    let result = `${Math.ceil(p)} px`;
    let scaleWidget = window.geo.gui.scaleWidget;
    if (scale && scaleWidget && scaleWidget.formatUnit) {
        let scaleresult = scaleWidget.formatUnit(p * scale, 'si', undefined, 4);
        if (scaleresult) {
            result += ` (${scaleresult})`;
        }
    }
    return result;
}

/**
 * Format an area as a string for the user.
 */
function areaStr(p, scale) {
    let result = `${Math.ceil(p)} px\xB2`;
    let scaleWidget = window.geo.gui.scaleWidget;
    if (scale && scaleWidget && scaleWidget.formatUnit) {
        let scaleresult = scaleWidget.formatUnit(p * scale * scale, 'si', scaleWidget.areaUnitsTable, 4);
        if (scaleresult) {
            result += ` (${scaleresult})`;
        }
    }
    return result;
}

/**
 * Format a rotation as a string for the user.
 */
function rotation(r) {
    return `${parseInt(r * 180 / Math.PI)}°`;
}

/**
 * Format a Date object as a localized string.
 */
function formatDate(s) {
    var d = new Date(s);
    return d.toLocaleString();
}

/**
 * This view behaves like a bootstrap "popover" that follows the mouse pointer
 * over the image canvas and dynamically updates according to the features
 * under the pointer.
 *
 * @param {object} [settings]
 * @param {number} [settings.debounce]
 *   Debounce time in ms for rerendering due to mouse movements
 */
var AnnotationPopover = View.extend({
    initialize(settings) {
        if (settings.debounce) {
            this._position = _.debounce(this._position, settings.debounce);
        }

        $('body').on('mousemove', '.h-image-view-body', (evt) => this._position(evt));
        $('body').on('mouseout', '.h-image-view-body', () => this._hide());
        $('body').on('mouseover', '.h-image-view-body', () => this._show());

        this._hidden = !settings.visible;
        this._users = {};
        this.collection = new ElementCollection();
        this.listenTo(this.collection, 'add', this._getUser);
        this.listenTo(this.collection, 'all', this.render);
        this.listenTo(events, 'h:imageOpened', this._bindMoveEvent);

        this._recomputeClosestElementThrottled = _.throttle(this._recomputeClosestElement, 100);
    },

    render() {
        if (!this._closestElement) {
            this.$el.html('');
        } else {
            const element = this._closestElement;
            const annotation = element.get('annotation');
            this.$el.html(
                annotationPopover({
                    annotations: [annotation],
                    elements: {[annotation.id]: [element]},
                    formatDate,
                    users: this._users,
                    elementProperties: (element) => this._elementProperties(element)
                })
            );
        }
        this._show();
        if (!this._visible()) {
            this._hide();
        }
        this._height = this.$('.h-annotation-popover').height();
        this._position();
        return this;
    },

    /**
     * Set the popover visibility state.
     *
     * @param {boolean} [show]
     *   if true: show the popover
     *   if false: hide the popover
     *   if undefined: toggle the popover state
     */
    toggle(show) {
        if (show === undefined) {
            show = this._hidden;
        }
        this._hidden = !show;
        this.render();
        return this;
    },

    /**
     * Check the local cache for the given creator.  If it has not already been
     * fetched, then send a rest request to get the user information and
     * rerender the popover.
     *
     * As a consequence to avoid always rendering asynchronously, the user name
     * will not be shown on the first render.  In practice, this isn't usually
     * noticeable.
     */
    _getUser(model) {
        var id = model.get('annotation').get('creatorId');
        if (!_.has(this._users, id)) {
            restRequest({
                url: 'user/' + id
            }).done((user) => {
                this._users[id] = user;
                this.render();
            });
        }
    },

    /**
     * Get an object containing elements that are to be
     * displayed to the user in a popover.  This object is
     * cached on the model to avoid recomputing these properties
     * every time they are displayed.
     */
    _elementProperties(element) {
        // cache the popover properties to reduce
        // computations on mouse move
        if (element._popover) {
            return element._popover;
        }

        function setIf(key, func = (v) => v) {
            const value = element.get(key);
            if (value) {
                let args = [value].concat(Array.prototype.slice.call(arguments, 2));
                props[key] = func.apply(this, args);
            }
        }

        const props = {};
        element._popover = props;

        if (element.get('label')) {
            props.label = element.get('label').value;
        }
        if (element.get('group')) {
            props.group = element.get('group');
        }
        let geojson = convert(element, {}).features[0];
        let geogeom = geojson.geometry;
        let area, edge, scale;
        if (geogeom.type === 'Polygon') {
            area = edge = 0;
            let lens = [];
            for (let j = 0; j < geogeom.coordinates.length; j += 1) {
                for (let i = 0; i < geogeom.coordinates[j].length - 1; i += 1) {
                    let v0 = geogeom.coordinates[j][i];
                    let v1 = geogeom.coordinates[j][i + 1];
                    area += (v1[1] - v0[1]) * (v0[0] + v1[0]) / 2 * (!j ? 1 : -1);
                    let len = ((v1[0] - v0[0]) ** 2 + (v1[1] - v0[1]) ** 2) ** 0.5;
                    edge += len;
                    lens.push(len);
                }
            }
            area = Math.abs(area);
            if ((geojson.properties.annotationType === 'ellipse' || geojson.properties.annotationType === 'circle') && edge) {
                area *= Math.PI / 4;
                const a = lens[0] / 2;
                const b = lens[1] / 2;
                const h = (a - b) ** 2 / (a + b) ** 2;
                // Ramanujan's approximation -- we actually need a series to
                // compute this properly.
                edge = Math.PI * (a + b) * (1 + 3 * h / (10 + (4 - 3 * h) ** 0.5));
            }
        }
        if (geogeom.type === 'LineString') {
            edge = 0;
            for (let i = 0; i < geogeom.coordinates.length - 1; i += 1) {
                let v0 = geogeom.coordinates[i];
                let v1 = geogeom.coordinates[i + 1];
                edge += ((v1[0] - v0[0]) ** 2 + (v1[1] - v0[1]) ** 2) ** 0.5;
            }
        }
        if (this && this.parentView && this.parentView.viewerWidget && this.parentView.viewerWidget._scale) {
            scale = this.parentView.viewerWidget._scale.scale;
        }
        setIf('center', point);
        setIf('width', length, scale);
        setIf('height', length, scale);
        setIf('radius', length, scale);
        setIf('rotation', rotation);
        if (area) {
            props.area = areaStr(area, scale);
        }
        if (edge) {
            props[geojson.type === 'LineString' ? 'length' : 'perimeter'] = length(edge, scale);
        }

        return props;
    },

    /**
     * Remove the hidden class on the popover element if this._visible()
     * returns true.
     */
    _show() {
        if (this._visible()) {
            this.$el.removeClass('hidden');
        }
    },

    /**
     * Unconditionally hide popover.
     */
    _hide() {
        this.$el.addClass('hidden');
    },

    /**
     * Determine if the popover should be visible.  Returns true
     * if there are active annotations under the mouse pointer and
     * the label option is enabled.
     */
    _visible() {
        return !this._hidden && this.collection.length > 0;
    },

    /**
     * Reset the position of the popover to the position of the
     * mouse pointer.
     */
    _position(evt) {
        if (evt) {
            this._lastPositionEvt = evt;
        } else {
            evt = this._lastPositionEvt;
        }
        if (evt && this._visible()) {
            this.$el.css({
                left: evt.pageX + 5,
                top: evt.pageY - this._height / 2
            });
        }
    },

    _distanceToElement(points) {
        const center = this._lastCenter;
        if (!center) {
            return 0;
        }
        let minimumDistance = Number.POSITIVE_INFINITY;
        // use an explicit loop for speed
        for (let index = 0; index < points.length; index += 1) {
            const point = points[index];
            const dx = point[0] - center.x;
            const dy = point[1] - center.y;
            const distance = dx * dx + dy * dy;
            minimumDistance = Math.min(minimumDistance, distance);
        }
        return minimumDistance;
    },

    _bindMoveEvent() {
        this.parentView.viewerWidget.viewer.geoOn(
            window.geo.event.mousemove, (evt) => {
                this._lastCenter = _.extend({}, evt.geo);
                this._recomputeClosestElementThrottled();
            }
        );
    },

    _recomputeClosestElement() {
        let minimumDistance = Number.POSITIVE_INFINITY;
        const lastElement = this._closestElement;
        this._closestElement = null;
        this.collection.each((e) => {
            let distance = 0;
            // Distance calculation is only valid for polylines, rectangles,
            // ellipses, and circle.  We should handle other annotations.
            // For ellipses and circles, we should take curvature into
            // account
            switch (e.get('type')) {
                case 'polyline':
                    distance = this._distanceToElement(e.get('points'));
                    break;
                case 'rectangle':
                    distance = this._distanceToElement(
                        convertRectangle(e.attributes).coordinates[0]
                    );
                    break;
                case 'ellipse':
                    distance = this._distanceToElement(
                        convertEllipse(e.attributes).coordinates[0]
                    );
                    break;
                case 'circle':
                    distance = this._distanceToElement(
                        convertCircle(e.attributes).coordinates[0]
                    );
                    break;
            }
            if (distance < minimumDistance) {
                this._closestElement = e;
                minimumDistance = distance;
            }
        });
        if (lastElement && this._closestElement && lastElement.id === this._closestElement.id) {
            // Don't rerender if the element didn't change;
            return;
        }
        this.render();
    }
});

export default AnnotationPopover;
