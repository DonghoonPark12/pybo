<script>
    let question_list = []

    function get_question_list() {
        fetch("http://127.0.0.1:8000/api/question/list").then((response) => {
            response.json().then((json) => {
                question_list = json
            })
        })
    }

    get_question_list()
    // let message, promise;

    // fetch("http://127.0.0.1:8000/hello").then(response => {
    //     response.json().then(json => {
    //         message = json.message;
    //     })
    // });

    // async function hello() {
    //     const res = await fetch("http://127.0.0.1:8000/hello");
    //     const json = await res.json();
    //
    //     if (res.ok) {
    //       return json.message;
    //     } else {
    //       alert("error");
    //     }
    // }
    //
    // promise = hello();
</script>

<!--{#await promise}-->
<!--  <p>...waiting</p>-->
<!--{:then message}-->
<!--  <h1>{message}</h1>-->
<!--{/await}-->

<!--<h1>{message}</h1>-->
<ul>
    {#each question_list as question}
        <li>{question.subject}</li>
    {/each}
</ul>

