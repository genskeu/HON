describe('Test register user', () => {
    it("test register new user", () => {
        cy.visit("/");
        cy.get("#register").click();
      
        cy.get("#username").type("test-user");
        cy.get("#password").type("test-user");
        cy.get("form").submit();
        cy.url().should('include', '/login')
    }),
    it("test login with new user", () => {     
        cy.visit("/");       
        cy.get("#username").type("test-user");
        cy.get("#password").type("test-user");
        cy.get("form").submit();
        cy.url().should('include', '/study/login')

        cy.get("#logout").click()
        cy.url().should('include', '/login')
    })
})

  
