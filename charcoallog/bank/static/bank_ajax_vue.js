Vue.component('all-reg-forms', {
    props: ['pk', 'date', 'money', 'description', 'category', 'payment'],
    template:`
            <div class="form-inline m-0 p-0">
                <input type="hidden" id="pk" name="pk" :value="pk">

                <div @input="n_dt">
                <input type="date" id="date" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :value="dt" :disabled="edit"
                       required>
                </div>

                <div @input="n_mn">
                <input type="number" id="money" name="money" step="0.01" class="form-inline m-0 p-0 bg-light"
                       size="11" style="font-size:10px;border:none"
                       :style="styleObject"
                       :value="mn" :disabled="edit"
                       required>
                </div>

                <div @input="n_description">
                <input type="text"  id="description" name="description" class="form-inline m-0 p-0 bg-light"
                       size="40" style="font-size:10px;border:none"
                       :value="dscrptn" :disabled="edit"
                       required>
                </div>

                <div @input="n_category">
                <input type="text"  id="category" name="category" class="form-inline m-0 p-0 bg-light"
                       size="6" style="font-size:10px;border:none"
                       :value="ctgr" :disabled="edit"
                       required>
                </div>

                <div @input="n_payment">
                <input type="text" id="payment" name="payment" class="form-inline m-0 p-0 bg-light"
                       size="15" style="font-size:10px;border:none"
                       :value="pmnt" :disabled="edit"
                       required>
                <input type="hidden" :value=this.payment name="old_payment">
                </div>

                <div class="form-inline m-0 p-0 bg-light">
                <input type="checkbox" id="checkbox" v-model:value="chk" v-bind="label()">
                <span class="form-text text-muted" style="font-size:9px">update</span>
                </div>

                <div class="form-inline m-0 p-0">
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" id="button" size="6" @click="dflt()">{{ method }}</button>
                </div>
            </div>
    `,
    data: function() {
        return {
            method: 'delete',
            edit: true,
            chk: false,
            pmnt: this.payment,
            ctgr: this.category,
            dscrptn: this.description,
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
        dflt: function() {
            this.chk = false
        },
        label: function(){
             this.method = this.chk ? 'update' : 'delete';
             this.edit = this.chk == false ? true : false
        },
    },
});

new Vue({
    el: "#vue_ajax",
    methods: {
        submitForm: function(event) {
            var old_payment = event.target.old_payment.value;
            console.log(old_payment + " HERE ")
            var form = {}
            form["pk"] = event.target.pk.value

            form["category"] = event.target.category.value;
            form["payment"] = event.target.payment.value;
            form["description"] = event.target.description.value;
            form["money"] = parseFloat(event.target.money.value);
            form["date"] = event.target.date.value;

            //if ( form['kind'].search('transfer') == -1 && kind != '---' ) {
            //event.target.checkbox.checked = false
            //}

            http_verb = event.target.button.innerText
            console.log(http_verb)
            http_verb = http_verb == 'delete' ? 'delete' : 'put'

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";

            axios({
                method: http_verb,
                url: 'home_api/' + form["pk"] + '/',
                data: form
            }).then(response => {
                // Check status code!


                if ( http_verb == 'delete' ) {

                    // DRF DELETE returns nothing
                    // math to update line1 data - minor

                    // whats_left_value - form_money
                    var current_whats_left_value = parseFloat(document.getElementById("left").textContent)
                    var left_atual_value = current_whats_left_value - form["money"]
                    document.getElementById("left").textContent = left_atual_value

                    // account_value - form_money
                    var current_account_value = parseFloat(document.getElementById(form["payment"]).textContent)
                    var account_atual_value = current_account_value - form["money"]
                    document.getElementById(form["payment"]).textContent = account_atual_value

                    document.getElementById(form["pk"]).remove()

                }

                if ( http_verb == 'put' ) {

                    if ( old_payment != form['payment']) {
                        console.log('old');
                        document.getElementById(old_payment).textContent = 0;
                        document.getElementById(old_payment+old_payment).remove();
                        //$("[class='"+old_payment+"']").remove();
                        //$("li[id='"+old_payment+old_payment+"']").remove();
                    }

                    $.each(response.data.accounts, function(index, value) {
                        console.log('iniciando loop');

                        if ($("[class='"+index+"").length < 1) {
                            // learn Vue
                            // creates a new account
                            var new_account = document.createElement('li');

                            new_account.id = index+index;
                            new_account.className = 'nav-item nav-link text-muted';
                            var text = '<div class="' + index + '">' + index + '<br><div id="' + index +'"><font size="2">' + value['money__sum'] + '</font></div></div>'
                            new_account.innerHTML = text;
                            var t = document.getElementsByTagName('ul')[1].appendChild(new_account);
                            //red_css(value['money__sum'], "[id='"+index+"']");
                        }
                        console.log(index);
                        document.getElementById(index).textContent = value['money__sum']
                        //$("[id='"+index+"']").text(value['money__sum']);
                        // red_css(value['money__sum'], "[id='"+index+"']");

                    });

                    document.getElementById("left").textContent = response.data.whats_left
                    //$("#left").text(content.whats_left);


                    // This works but does not create new account
                    // console.log(response)
                    // update line1 data - math already done by Django
                    // if account does not exits create one missing - TODO
                    // var account = response.data.accounts[form["payment"]]
                    // document.getElementById(form["payment"]).textContent = account["money__sum"]

                    // document.getElementById("left").textContent = response.data.whats_left
                }
            })
            .catch(function (err) {
                console.log(err.message);
            })
        }
    }
})
