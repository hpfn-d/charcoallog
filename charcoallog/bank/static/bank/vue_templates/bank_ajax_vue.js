Vue.component('all-reg-forms', {
    //props: ['color', 'csrf','pk', 'date', 'money', 'description', 'category', 'payment'],
    props: ['color', 'csrf', 'data', 'url_api'],
    template:`
            <form @submit.prevent="submitForm($event)" :id="pk">

            <div class="form-inline m-0 p-0">

                <input type="hidden" name="csrfmiddlewaretoken" :value="token">
                <input type="hidden" id="pk" name="pk" :value="pk">

                <div @input="n_dt">
                <input type="date" id="date" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="11" style="font-size:10px;border:none"
                       :value="dt" :disabled="edit"
                       required>
                </div>

                <div @input="n_mn">
                <input type="text" id="money" name="money" step="0.01" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="11" style="font-size:10px;border:none"
                       :style="styleObject"
                       :value="mn" :disabled="edit"
                       required>
                </div>

                <div @input="n_description">
                <input type="text"  id="description" name="description" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="20" style="font-size:10px;border:none"
                       :value="dscrptn" :disabled="edit"
                       required>
                </div>

                <div @input="n_category">
                <input type="text"  id="category" name="category" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="20" style="font-size:10px;border:none"
                       :value="ctgr" :disabled="edit"
                       required>
                </div>

                <div @input="n_payment">
                <input type="text" id="payment" name="payment" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(data.fields.money)}"
                       size="20" style="font-size:10px;border:none"
                       :value="pmnt" :disabled="edit"
                       required>
                <input type="hidden" :value=this.data.fields.payment name="old_payment">
                </div>

                <div class="form-inline m-0 p-0 bg-light" v-if="!isNaN(mn)">
                <input type="checkbox" id="checkbox" v-model:value="chk" v-bind="label()">
                <span class="form-text text-muted" style="font-size:9px">update</span>
                </div>

                <div class="form-inline m-0 p-0" v-if="!isNaN(mn)">
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" id="button" size="6" @click="dflt()">{{ method }}</button>
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
            pmnt: this.data.fields.payment,
            ctgr: this.data.fields.category,
            dscrptn: this.data.fields.description,
            mn: this.data.fields.money,
            dt: this.data.fields.date,
            pk: this.data.pk,
            to_url: this.url_api.replace('10101010', this.data.pk)
        }
    },
    computed: {
        styleObject() {
            var font_color =  this.mn > 0 ?  'black' : 'red';
            return {
                color: this.color ? this.color : font_color
            };
        },
    },
    methods:{
        n_category: function(event) {
            this.ctgr = event.target.value
        },
        n_payment: function(event) {
            this.pmnt = event.target.value
        },
        n_description: function(event) {
             this.dscrptn = event.target.value
        },
        n_mn: function(event) {
             this.mn = event.target.value
        },
        n_dt: function(event) {
            this.dt = event.target.value
        },
        dflt: function() { // this will change for Vue 2.6.0 - rm
            this.chk = false
        },
        label: function(){
            this.method = this.chk ? 'update' : 'delete';
            this.edit = this.chk == false ? true : false
        }, // schedule stuff - axios
        schedule_del: function(money, pk){
            var current_whats_left_value = Number(document.getElementById("schedule_whats_left").textContent)
            var left_atual_value = parseFloat(current_whats_left_value - money)

            document.getElementById("schedule_whats_left").textContent = left_atual_value
            document.getElementById(pk).remove()
        },
        schedule_put: function(w_left){
            document.getElementById('schedule_whats_left').textContent = w_left
        }, // extract stuff - axios
        extract_del: function(money, payment, pk){
            // whats_left_value - form_money
            var current_whats_left_value = Number(document.getElementById("left").textContent)
            var left_atual_value = parseFloat(current_whats_left_value - money)
            document.getElementById("left").textContent = left_atual_value
            // account_value - form_money
            var current_account_value = Number(document.getElementById(payment).textContent)
            var account_atual_value = parseFloat(current_account_value - money)
            document.getElementById(payment).textContent = account_atual_value
            document.getElementById(pk).remove()
        },
        extract_put: function(accounts, w_left, old_payment, payment){

            if ( old_payment != payment) {
                document.getElementById(old_payment).textContent = 0;
                document.getElementById(old_payment+old_payment).remove();
            }

            $.each(accounts, function(index, value) {
                if ($("[id='"+index+"").length < 1) {
                    // creates a new account
                    var new_account = document.createElement('li');

                    new_account.id = index+index;
                    new_account.className = 'nav-item nav-link';
                    var text = index + '<br><span id="' + index +'">' + value['money__sum'] + '</span>'
                    new_account.innerHTML = text;
                    var t = document.getElementsByTagName('ul')[1].appendChild(new_account);
                }
                document.getElementById(index).textContent = value['money__sum']
            });
            document.getElementById("left").textContent = w_left
        },
        submitForm: function(event) {
            var old_payment = event.target.old_payment.value;

            var form = {}
            form["pk"] = Number(event.target.pk.value)
            form["category"] = event.target.category.value
            form["payment"] = event.target.payment.value
            form["description"] = event.target.description.value
            form["money"] = Number(event.target.money.value)
            form["date"] = event.target.date.value

            // vue 2.6.0
            //event.target.checkbox.checked = false
            // change button too. After http_verb

            http_verb = event.target.button.innerText
            http_verb = http_verb == 'delete' ? 'delete' : 'put'

            //axios.defaults.baseURL = 'http://';
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";

            axios({
                method: http_verb,
                url: this.to_url,
                data: form,
            }).then(response => {
                var has_schdl_api = this.to_url.indexOf('schedule_api')
                var has_home_api =  this.to_url.indexOf('home_api')

                if ( http_verb == 'delete' && response.status == 204) {
                    if (has_schdl_api >= 0) {
                        this.schedule_del(form["money"], form["pk"])
                    }
                    if (has_home_api >= 0) {
                        this.extract_del(form["money"], form["payment"], form["pk"])
                    }
                }
                if ( http_verb == 'put' && response.status == 200) {
                    if (has_schdl_api >= 0) {
                        var w_left = response.data
                        this.schedule_put(w_left)
                    }
                    if (has_home_api >= 0) {
                        var accounts = response.data.accounts
                        var w_left = response.data.whats_left
                        this.extract_put(accounts, w_left, old_payment, form["payment"])
                    }
                }
            })
            .catch(function (err) {
                console.log(err.message);
            })
        }
    },
});
