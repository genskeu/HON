describe('Test create study', () => {
    it("login study admin", () => {
        cy.visit("/");
        cy.url().should('include', '/login')

        cy.get("#username").type("sadmin");
        cy.get("#password").type("sadmin");
        cy.get("form").submit();
    }),
    it("create study", () => {     
        cy.get("#create-study").click();
        cy.url().should('include', '/metainfos')
    }),
    it("change study metainfos", () => {     
    }),
    it("upload files", () => {     
    }),
    it("create image-sets", () => {     
    }),
    it("add scales", () => {     
    })
})