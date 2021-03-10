import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
// import mutation from './mutation'

Vue.use(Vuex)

import createLogger from "vuex/dist/logger";
const debug = process.env.NODE_ENV !== "production";

const store = new Vuex.Store({
    state: {
        colors: [],
        change_records: [],
        unsaved_changes: [],
        current_step: 0,
        autoSave: true,
        current_tag_idx: [0, 0],
    },
    getters: {
        current_color_idx: (state, getters) => {
            let idx = 0
            for (let i = 0; i < state.current_tag_idx[0]; i++) {
                idx += getters.basic_tags[i].length
            }
            return idx + state.current_tag_idx[1]
        },
        idx_to_color: (state, getters) => ([medium_idx, basic_idx]) => {
            let medium = getters.color_medium(getters.medium_tags[medium_idx][0]), basic
            if (basic_idx != -1) {
                basic = getters.color_basic(getters.basic_tags[medium_idx][basic_idx][0])
            }
            return [medium, basic]
        },
        current_color: (state, getters) => {
            return getters.idx_to_color(state.current_tag_idx)
        },
        medium_tags: (state) => {
            // console.log('medium_tags', state.colors)
            return state.colors.slice(0, state.colors.length).map(item => [item[0], item[1]])
        },
        basic_tags: state => {
            return state.colors.slice(0, state.colors.length).map(item => item[2].map(it => [it[0], it[1]]))
        },
        color_tags: state => {
            let tmp = state.colors.slice(0, state.colors.length).map(item => item[2].map(it => it[2]))
            let target = []
            for (let i = 0; i < tmp.length; i++) {
                target = target.concat(tmp[i])
            }
            return target
        },
        color_medium: state => medium_tag => {
            return state.colors.find(item => item[0] == medium_tag)
        },
        color_basic: state => (basic_tag) => {
            // console.log('color_basic', state, basic_tag)
            for (let i = 0; i < state.colors.length; i++) {
                let basic = state.colors[i][2].find(item => item[0] == basic_tag)
                if (basic) {
                    return basic
                }
            }
        },
    },
    mutations: {
        freshColors(state, payload) {
            state.colors = payload.colors
        },
        set_autoSave(state, val) {
            state.autoSave = val
        },
        set_current_tag_idx(state, val) {
            state.current_tag_idx = val
        },
        set_active_idx(state, val) {
            state.active_idx = val
        },
        newRecord(state, record) {
            state.change_records.splice(
                state.current_step,
                state.change_records.length - state.current_step,
                record
            );
        },
        newUnsavedChange(state, record) {
            let [current, target] = [record.current, record.target]
            if (record.opType == 'color') {
                [record.current, record.target] = [current[0], target[0]]
            }
            else if (record.opType == 'basic') {
                if (current == -1) {
                    record.target = [target[0][0], target[1]]
                }
                else if (target == -1) {
                    record.current = current[1][0]
                }
                else {
                    record.current = current[1][0]
                    record.target = target[0][0]
                }
            }
            state.unsaved_changes.push(record);
        }
    },
    actions: {

        makeRecord(context, payload) {
            let [ifSave, newRecord, plus] = payload.save;
            if (!ifSave) {
                return;
            }
            if (newRecord) {
                context.commit('newRecord', payload.record)
            }
            if (plus) {
                context.state.current_step++;
            } else {
                context.state.current_step--;
            }
            context.commit('newUnsavedChange', JSON.parse(JSON.stringify(payload.record)))
            if (context.state.autoSave) {
                context.dispatch('save')
            }
        },
        save(context) {
            if (context.state.unsaved_changes.length == 0) {
                alert("没有需要保存的对象");
                return;
            }
            let params = new URLSearchParams();
            params.set("changeRecords", JSON.stringify(context.state.unsaved_changes));
            axios.post("/colorClassifier/changeColor", params)
                .then((response) => {
                    context.state.unsaved_changes = [];
                    console.log(response);
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        opColor(context, payload) {
            // let start = new Date().getTime() / 1000
            console.log('opC', payload)
            let save = payload.save ? payload.save : [true, true, true]
            let [current, target, bgcs] = [payload.current, payload.target, payload.bgcs]
            for (let i = 0; i < bgcs.length; i++) {
                let bgc = bgcs[i];
                Vue.set(target[2], target[2].length, bgc)
                Vue.delete(current[2], current[2].indexOf(bgc))
            }
            context.dispatch('makeRecord', {
                record: {
                    current: payload.current,
                    target: payload.target,
                    bgcs: bgcs,
                    opType: 'color'
                },
                save: save
            })
            // console.log(new Date().getTime() / 1000 - start)
        },
        opColorBasic(context, payload) {

            console.log('opCB', payload)
            let save = payload.save ? payload.save : [true, true, true]
            if (payload.target == -1) {
                let [current_medium, current_basic] = payload.current
                Vue.delete(current_medium[2], current_medium[2].indexOf(current_basic))
                context.commit('set_current_tag_idx', [context.state.current_tag_idx[0], 0])
            }
            else if (payload.current == -1) {
                let target_medium = payload.target[0]
                Vue.set(target_medium[2], target_medium[2].length, payload.target[1])

            }
            else {
                let [current_medium, current_basic, target_medium] = [payload.current[0], payload.current[1], payload.target[0]]
                console.log(current_medium, current_basic, target_medium)
                Vue.set(target_medium[2], target_medium[2].length, current_basic)
                Vue.delete(current_medium[2], current_medium[2].indexOf(current_basic))
                context.commit('set_current_tag_idx', [context.state.colors.indexOf(target_medium), target_medium[2].length - 1])
            }
            context.dispatch('makeRecord', {
                record: {
                    current: payload.current,
                    target: payload.target,
                    opType: 'basic'
                },
                save: save
            })
        },
        opColorMedium(context, payload) {
            console.log('opCM', payload)
            let save = payload.save ? payload.save : [true, true, true]
            if (payload.current == -1) {
                context.state.colors.splice(0, 0, payload.target)
            }
            else if (payload.target == -1) {
                let current_medium = payload.current
                context.state.colors.splice(context.state.colors.indexOf(current_medium), 1)
            }
            context.dispatch('makeRecord', {
                record: {
                    current: payload.current,
                    target: payload.target,
                    opType: 'medium'
                },
                save: save
            })
        },
        revoke(context) {
            if (context.state.current_step == 0) {
                alert("没有可以撤销的对象");
                return;
            }
            let re_record = context.state.change_records[context.state.current_step - 1];
            console.log('revoke', re_record)
            if (re_record.opType == 'medium') {
                context.dispatch('opColorMedium', { current: re_record.target, target: re_record.current, opType: 'medium', save: [true, false, false] })
            }
            else if (re_record.opType == 'basic') {
                context.dispatch('opColorBasic', { current: re_record.target, target: re_record.current, opType: 'basic', save: [true, false, false] });
            }
            else if (re_record.opType == 'color') {
                context.dispatch('opColor', { current: re_record.target, target: re_record.current, bgcs: re_record.bgcs, opType: 'color', save: [true, false, false] });
            }
            else {
                console.log('REVOKE ERROR*********', re_record)
            }
        },
        restore(context) {
            if (context.state.current_step == context.state.change_records.length) {
                alert("没有可以恢复的对象");
                return;
            }

            let re_record = context.state.change_records[context.state.current_step];
            console.log('restore', re_record)
            if (re_record.opType == 'medium') {
                context.dispatch('opColorMedium', { ...re_record, save: [true, false, true] })
            }
            else if (re_record.opType == 'basic') {
                context.dispatch('opColorBasic', { ...re_record, save: [true, false, true] });
            }
            else if (re_record.opType == 'color') {
                context.dispatch('opColor', { ...re_record, save: [true, false, true] });
            }
            else {
                console.log('RESTORE ERROR*********', re_record)
            }
        },
    },
    plugins: debug ? [createLogger()] : []
})

export default store