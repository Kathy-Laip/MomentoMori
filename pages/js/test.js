import User from ".";

describe("authorization", function(){
    it("test person one", function(){
        let user = new User({login: "AAA", password: "dekanatlohi"})
        user.authorization()
        assert.equal()
    })
})