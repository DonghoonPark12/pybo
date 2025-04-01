<script>
    import Router from 'svelte-spa-router'
    import Home from "./routes/Home.svelte"
    import Detail from "./routes/Detail.svelte"
    import QuestionCreate from "./routes/QuestionCreate.svelte"
    import Navigation from "./components/Navigation.svelte"
    import UserCreate from "./routes/UserCreate.svelte"
    import UserLogin  from "./routes/UserLogin.svelte"

    const routes = {
        // / 주소에 매핑되는 컴포넌트로 <Home />을 등록
        // 여기서 <Home />은 새로 작성한 Home.svelte 파일의 내용을 의미
        '/': Home,
        '/detail/:question_id': Detail,
        '/question-create': QuestionCreate,
        '/user-create': UserCreate,
        '/user-login': UserLogin,

    }
</script>

<Navigation />
<Router {routes} />