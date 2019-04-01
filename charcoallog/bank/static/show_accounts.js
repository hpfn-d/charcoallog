var bus = new Vue({});


// var brief = new Vue({
//     el: "#line1_accounts",
//     data: {
//         line1_accounts_brief: ''
//     }
// });

var brief = new Vue({
    el: "#line1_accounts",
    data: {
        out: {},
        whats_left: parseFloat(document.getElementById("left").textContent)
    },
    computed: {
        styleObject() {
            var font_color = 'black';
            if (this.vl < 0)
                font_color = 'red';
            return {
                color: font_color
            };
        },
    },
    methods: {
        account_call: function(event) {

            this.whats_left = parseFloat(document.getElementById("left").textContent)
            var num_ = parseFloat(event.target.lastChild.innerText)
            //console.log(event)
            //console.log(event.target.id)
            //console.log(num_)
            //console.log('tem chave')
            //console.log(this.out.hasOwnProperty(event.target.id))

            var key_ = event.target.id
            var len_key_ = key_.length / 2
            key_ = key_.slice(0,len_key_)


            if (this.out.hasOwnProperty(event.target.id)) {
                //console.log('mais')
                //console.log(this.whats_left, num_)
                document.getElementById("left").textContent = this.whats_left + num_
                document.getElementById(key_).style.color = 'black'
                //console.log('ative')
                //console.log(event.target.id)
                delete this.out[event.target.id]

            } else {
                //console.log('menos')
                //console.log(this.whats_left, num_)
                document.getElementById("left").textContent = this.whats_left - num_
                document.getElementById(key_).style.color = 'purple'
                this.out[event.target.id] = 'inative'

            }
            //console.log(this.out)

            //this.whats_left = parseFloat(document.getElementById("left").textContent)
        },
    },
});


var bank_ajax = new Vue({
    el: "#vue_ajax",
    methods: {
        submitForm: function(event) {
            var old_payment = event.target.old_payment.value;
            //console.log(old_payment + " HERE ")
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
            //console.log(http_verb)
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
                        //console.log('iniciando loop');
                        //console.log(index)

                        if ($("[id='"+index+"").length < 1) {
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


