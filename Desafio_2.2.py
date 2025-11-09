

def menu():
    menu_text = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo Usuário
[5] Nova Conta
[0] Sair

=> """
    return input(menu_text)

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("✔ Sucesso na Operação")
    else:
        print("✖ Falha na Operação: valor inválido")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_de_saques, limite_de_saques):
    ultrapassou_saldo = valor > saldo
    ultrapassou_limite = valor > limite
    ultrapassou_saques = numero_de_saques >= limite_de_saques

    if ultrapassou_saldo:
        print("Falha! Saldo insuficiente.")
        return saldo, extrato, numero_de_saques

    if ultrapassou_limite:
        print("Falha! Limite ultrapassado.")
        return saldo, extrato, numero_de_saques

    if ultrapassou_saques:
        print("Falha! Limite de saques excedido.")
        return saldo, extrato, numero_de_saques

    if valor > 0:
        saldo += valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_de_saques += 1
        print("✔ Saque realizado com sucesso.")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_de_saques

def mostrar_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def filtrar_usuario(cpf, usuarios):
    encontrados = [u for u in usuarios if u.get("cpf") == cpf]
    return encontrados[0] if encontrados else None

def criar_usuario(usuarios):
    cpf = input("Informe seu CPF (Somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("CPF já cadastrado.")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de Nascimento (D-M-A): ")
    endereco = input("Endereço (Cidade + Sigla de Estado, Bairro, Nº): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "cpf": cpf
    })

    print("Usuário criado com sucesso.")

def criar_conta_bancaria(agencia, numero_de_conta, usuarios):
    cpf = input("Informe seu CPF (Somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Conta criada com sucesso.")
        return {"agencia": agencia, "numero_conta": numero_de_conta, "usuario": usuario}
    print("Usuário não encontrado.")
    return None

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for c in contas:
        print(f"Agência: {c['agencia']} | Conta: {c['numero_conta']} | Titular: {c['usuario']['nome']}")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0.0
    limite = 500.0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            try:
                valor = float(input("Deposite: "))
            except ValueError:
                print("Valor inválido.")
                continue
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            try:
                valor = float(input("Saque: "))
            except ValueError:
                print("Valor inválido.")
                continue
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_de_saques=numero_saques,
                limite_de_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta_bancaria(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            print("Encerrando... Até mais!")
            break

        else:
            print("ERRO, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()


