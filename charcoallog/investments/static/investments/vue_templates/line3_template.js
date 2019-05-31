Vue.component('all-reg-forms', {
    // props: ['pk', 'date', 'money', 'kind', 'tx_op', 'brokerage'],
    props: ['csrf', 'data'],  // color? no schedule here
    template:`
        <form @submit.prevent="submitForm($event)" :id="pk">


            <div class="form-inline m-0 p-0">
                <input type="hidden" name="csrfmiddlewaretoken" :value="token">
                <input type="hidden" id="pk" name="pk" :value="pk">

                <div @input="n_dt">
                <input type="date" id="date" class="form-inline bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="10" style="font-size:10px;border:none"
                       :value="dt"
                       :disabled="edit">
                </div>

                <div @input="n_mn">
                <input type="text" id="money"class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="11" style="font-size:10px;border:none"
                       :style="styleObject"
                       :value="mn"
                       :disabled="edit">
                </div>

                <div @input="n_knd">
                <input type="text"  id="kind" name="kind" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="25" style="font-size:10px;border:none"
                       :value="knd"
                       :disabled="edit">
                </div>

                <div @input="n_whch_trgt" v-if="this.data.fields.which_target">
                <input type="text" id="which_target" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="15" style="font-size:10px;border:none"
                       :value="whch_trgt"
                       :disabled="edit">
                </div>

                <div @input="n_sgmnt" v-if="this.data.fields.segment">
                <input type="text" id="segment" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="20" style="font-size:10px;border:none"
                       :value="sgmnt"
                       :disabled="edit">
                </div>

                <div @input="n_tx_op" v-if="this.data.fields.tx_op">
                <input type="text"  id="tx_op" name="tx_op" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="6" style="font-size:10px;border:none"
                       :value="tx_op"
                       :disabled="edit">
                </div>

                <div @input="n_brkrg" v-if="this.data.fields.brokerage">
                <input type="text" id="brokerage" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="15" style="font-size:10px;border:none"
                       :value="brkrg"
                       :disabled="edit">
                 </div>

                <div @input="n_tx_r_prc" v-if="this.data.fields.tx_or_price">
                <input type="text" id="tx_or_price" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="6" style="font-size:10px;border:none"
                       :value="tx_r_prc"
                       :disabled="edit">
                </div>

                <div @input="n_qunt" v-if="this.data.fields.quant">
                <input type="text" id="quant" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size='4' style="font-size:10px;border:none"
                       :value="qunt"
                       :disabled="edit">
                </div>

                <div v-if="!isNaN(mn)">
                <div class="form-inline m-0 p-0 bg-light" v-if="this.data.fields.kind != '---'">
                <input type="checkbox" id="checkbox" v-model:value="chk" v-bind="label()">
                <span class="form-text text-muted" style="font-size:9px">update</span>
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" size="6" id="button" @click="dflt()">{{ method }}</button>
                </div>
                </div>
                <div v-else class="form-inline m-0 p-0 bg-light">
                <input size='12'
                style="font-size:10px;border:none;background-color:lightgrey"
                value='what to do next'>
                </div>
            </div>
        </form>
    `,
    data: function() {
        return {
            method: 'delete',
            edit: true,
            chk: false,
            token: this.csrf,
            qunt: this.data.fields.quant,
            tx_r_prc: this.data.fields.tx_or_price,
            tx_op: this.data.fields.tx_op,
            sgmnt: this.data.fields.segment,
            whch_trgt: this.data.fields.which_target,
            brkrg: this.data.fields.brokerage,
            knd: this.data.fields.kind,
            mn: this.data.fields.money,
            dt: this.data.fields.date,
            pk: this.data.pk
        }
    },
    computed: {
        styleObject() {
            var font_color =  this.mn > 0 ?  'black' : 'red';
            return {
                color: font_color
            };
        }
    },
    methods:{
        n_brkrg: function(event) {
            this.brkrg = event.target.value
        },
        n_qunt: function(event) {
            this.qunt = event.target.value
        },
        n_tx_r_prc: function(event) {
            this.tx_r_prc = event.target.value
        },
        n_tx_op: function(event) {
            this.tx_op = event.target.value
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
             console.log(this.mn)
             this.method = this.chk ? 'update' : 'delete';
             this.edit = this.chk == false ? true : false
        },
        submitForm: function(event) {
            var form = {}
            form["pk"] = Number(event.target.pk.value);
            form["date"] = event.target.date.value;
            form["money"] = Number(event.target.money.value);
            form["kind"] = event.target.kind.value;
            // not in details
            if (event.target.hasOwnProperty('tx_op')) {
                form["tx_op"] = Number(event.target.tx_op.value);
                form["brokerage"] = event.target.brokerage.value;
            }
            
            _url = '/investments/home_api/'

            // details
            if (event.target.hasOwnProperty('tx_or_price')) {
                form["tx_or_price"] = Number(event.target.tx_or_price.value);
                form["segment"] = event.target.segment.value;
                form["which_target"] = event.target.which_target.value;
                form['quant'] = Number(event.target.quant.value);
                _url = '/investments/details/detail_api/'
            }
            
            event.target.checkbox.checked = false
            http_verb = event.target.button.innerText
            http_verb = http_verb == 'delete' ? 'delete' : 'put'

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";

            axios({
                method: http_verb,
                url: _url + form["pk"] + '/',
                data: form
            })
            .then(response => {
                // status code
                if ( http_verb == 'delete' && response.status == 204 ) {
                    document.getElementById(form["pk"]).remove()
                }
            })
            .catch(function (err) {
               console.log(err.message);
            })
        }
    },
});