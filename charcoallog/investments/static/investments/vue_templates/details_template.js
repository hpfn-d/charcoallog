Vue.component('all-detail-forms', {
    props: ['pk', 'date', 'money', 'kind', 'which_target', 'segment', 'tx_or_price', 'quant'],
    template:`
            <div class="form-inline m-0 p-0">
                <input type="hidden" id="pk" name="pk" :value="pk">

                <div @input="n_dt">
                <input type="date" id="date" class="form-inline bg-light"
                       size="10" style="font-size:10px;border:none"
                       :value="dt"
                       :disabled="edit">
                </div>

                <div @input="n_mn">
                <input type="text" id="money"class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :style="styleObject"
                       :value="mn"
                       :disabled="edit">
                </div>

                <div @input="n_knd">
                <input type="text"  id="kind" name="kind" class="form-inline m-0 p-0 bg-light"
                       size="25" style="font-size:10px;border:none"
                       :value="knd"
                       :disabled="edit">
                </div>

                <div @input="n_whch_trgt">
                <input type="text" id="which_target" class="form-inline m-0 p-0 bg-light"
                       size="15" style="font-size:10px;border:none"
                       :value="whch_trgt"
                       :disabled="edit">
                </div>

                <div @input="n_sgmnt">
                <input type="text" id="segment" class="form-inline m-0 p-0 bg-light"
                       size="20" style="font-size:10px;border:none"
                       :value="sgmnt"
                       :disabled="edit">
                </div>

                <div @input="n_tx_r_prc">
                <input type="text" id="tx_or_price" class="form-inline m-0 p-0 bg-light"
                       size="6" style="font-size:10px;border:none"
                       :value="tx_r_prc"
                       :disabled="edit">
                </div>
                <div @input="n_qunt">
                <input type="text" id="quant" class="form-inline m-0 p-0 bg-light"
                       size='4' style="font-size:10px;border:none"
                       :value="qunt"
                       :disabled="edit">
                </div>

                <div class="form-inline m-0 p-0">
                <input type="checkbox" id="checkbox" v-model:value="chk" v-bind="label()">
                <span class="form-text text-muted" style="font-size:9px">update</span>
                </div>

                <!--<div v-if="chk == true" class="form-inline m-0 p-0">-->
                <div class="form-inline m-0 p-0">
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" size="6" id="button" @click="dflt()">{{ method }}</button>
                </div>
            </div>
    `,
     data: function() {
         return {
             method: 'delete',
             edit: true,
             chk: false,
             qunt: this.quant,
             tx_r_prc: this.tx_or_price,
             sgmnt: this.segment,
             whch_trgt: this.which_target,
             knd: this.kind,
             mn: this.money,
             dt: this.date
         }
    },
    computed: {
        styleObject() {
            var font_color = 'red';
            if (this.mn < 0)
                font_color = 'blue';
            return {
                color: font_color
            };
        }
    },
    methods:{
        n_qunt: function(event) {
            this.qunt = event.target.value
        },
        n_tx_r_prc: function(event) {
            this.tx_r_prc = event.target.value
        },
        n_sgmnt: function(event) {
            this.sgmnt = event.target.value
        },
        n_whch_trgt: function(event) {
            this.whch_trgt = event.target.value
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
