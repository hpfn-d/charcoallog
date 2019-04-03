Vue.component('all-reg-forms', {
    props: ['pk', 'date', 'money', 'kind', 'tx_op', 'brokerage'],
    template:`
            <div class="form-inline m-0 p-0">
                <input type="hidden" id="pk" name="pk" :value="pk">

                <div @input="n_dt">
                <input type="date" id="date" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :value="dt"
                       :disabled="edit">
                </div>

                <div @input="n_mn">
                <input type="number" id="money" name="money" step="0.01" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :style="styleObject"
                       :value="mn"
                       :disabled="edit">
                </div>

                <div @input="n_knd">
                <input type="text"  id="kind" name="kind" class="form-inline m-0 p-0 bg-light"
                       size="40" style="font-size:10px;border:none"
                       :value="knd"
                       :disabled="edit">
                </div>

                <div @input="n_tx_p">
                <input type="text"  id="tx_op" name="tx_op" class="form-inline m-0 p-0 bg-light"
                       size="6" style="font-size:10px;border:none"
                       :value="tx_p"
                       :disabled="edit">
                </div>

                <div @input="n_brkrg">
                <input type="text" id="brokerage" class="form-inline m-0 p-0 bg-light"
                       size="15" style="font-size:10px;border:none"
                       :value="brkrg"
                       :disabled="edit">
                </div>

                <div class="form-inline m-0 p-0 bg-light" v-if="kind.search('transfer') == -1 && kind != '---'">
                <input type="checkbox" id="checkbox" v-model:value="chk" v-bind="label()">
                <span class="form-text text-muted" style="font-size:9px">update</span>
                </div>


                <div v-if= "kind != '---'" class="form-inline m-0 p-0">
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" id="button" size="6" @click="dflt()">{{ method }}</button>
                </div>
            </div>
    `,
    data: function() {
        return {
            method: 'delete',
            edit: true,
            chk: false,
            brkrg: this.brokerage,
            tx_p: this.tx_op,
            knd: this.kind,
            mn: this.money,
            dt: this.date
        }
    },
    computed: {
        styleObject() {
            var font_color = 'black';
            if (this.mn < 0)
                font_color = 'red';
            return {
                color: font_color
            };
        }
    },
    methods:{
        n_tx_p: function(event) {
            this.tx_p = event.target.value
        },
        n_brkrg: function(event) {
            this.brkrg = event.target.value
        },
        n_knd: function(event) {
             this.knd = event.target.value
        },
        n_mn: function(event) {
             this.mn = event.target.value
        },
        n_dt: function(event) {
            this.dt = event.target.value
        },
        dflt: function() {
            this.chk = false
        },
        label: function(){
             this.method = this.chk ? 'update' : 'delete';
             this.edit = this.chk == false ? true : false
        },
    },
});