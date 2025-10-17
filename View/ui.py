from presentation.account_vm import CuentaViewModel


class CuentaCLIView:
    """Vista CLI: suscribe a observables y expone un loop simple de demo."""

    def __init__(self, vm: CuentaViewModel):
        self.vm = vm
        self.vm.balance.subscribe(self._render_balance)
        self.vm.error.subscribe(self._render_error)
        self.vm.mensaje.subscribe(self._render_mensaje)

    def _render_balance(self, saldo):
        print(f"Saldo actual: {saldo}")

    def _render_error(self, err):
        if err:
            print(f"[ERROR] {err}")

    def _render_mensaje(self, msg):
        if msg:
            print(f"[INFO] {msg}")

    def demo(self):
        print("=== Demo CLI Cuenta (MVVM + Firebase) ===")
        print(
            "Comandos: d <monto> | r <monto> <pin> | new <num> <titular> <pin> | save | load <num> | del <num> | list | h | q"
        )
        while True:
            try:
                entrada = input("> ").strip()
            except EOFError:
                break
            if not entrada:
                continue
            if entrada.lower() == "q":
                break
            if entrada.lower() in ("h", "help", "ayuda"):
                print(
                    "Comandos: d <monto> | r <monto> <pin> | new <num> <titular> <pin> | save | load <num> | del <num> | list | q"
                )
                continue
            partes = entrada.split()
            cmd = partes[0].lower()
            if cmd in ("d", "depositar") and len(partes) == 2:
                try:
                    monto = float(partes[1].replace(",", "."))
                    self.vm.depositar(monto)
                except ValueError:
                    print("Uso: d <monto>  |  depositar <monto>")
            elif cmd in ("r", "retirar") and len(partes) == 3:
                try:
                    monto = float(partes[1].replace(",", "."))
                    self.vm.retirar(monto, partes[2])
                except ValueError:
                    print("Uso: r <monto> <pin>  |  retirar <monto> <pin>")
            elif cmd == "new" and len(partes) >= 4:
                # new <numero> <titular con espacios...> <pin>
                numero = partes[1]
                pin = partes[-1]
                titular = " ".join(partes[2:-1])
                try:
                    from domain.account import CuentaBancaria

                    self.vm._cuenta = CuentaBancaria(numero, titular, pin)
                    self.vm.balance.value = self.vm._cuenta.saldo
                    self.vm.mensaje.value = f"Cuenta creada localmente: {numero}"
                except Exception as exc:
                    print(f"Error creando cuenta: {exc}")
            elif cmd == "save":
                self.vm.guardar()
            elif cmd == "load" and len(partes) == 2:
                self.vm.cargar(partes[1])
            elif cmd == "del" and len(partes) == 2:
                self.vm.eliminar(partes[1])
            elif cmd == "list":
                items = self.vm.listar()
                if not items:
                    print("(sin elementos)")
                else:
                    for k, v in items.items():
                        print(f"- {k}: {v}")
            else:
                print("Comando no reconocido. Escribe 'h' para ayuda.")


