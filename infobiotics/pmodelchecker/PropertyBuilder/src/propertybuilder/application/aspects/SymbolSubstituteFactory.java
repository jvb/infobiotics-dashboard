package propertybuilder.application.aspects;

import java.util.ArrayList;
import java.util.LinkedList;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JTextField;
import propertybuilder.application.ApplicationContext;
import propertybuilder.application.ApplicationData;
import propertybuilder.pattern.IVariable;
import propertybuilder.pattern.InputElement;
import propertybuilder.pattern.Literal;
import propertybuilder.pattern.Symbol;
import propertybuilder.pattern.SymbolSequence;
import propertybuilder.pattern.SymbolType;
import propertybuilder.pattern.Variable;
import propertybuilder.pattern.VariableType;

/**
 * 
 * @author Ciprian
 */
public class SymbolSubstituteFactory {

	private ApplicationData appData;
	private ApplicationContext ctx;
	public static int DEFAULT_POOL_SIZE = 20;
	private int definedPoolSize = 0;
	private LinkedList<ComboBoxInput> cbQueue;
	private LinkedList<TextFieldInput> tfQueue;
	private LinkedList<JLabel> labelQueue;
	private LinkedList<SymbolSubstituteListener> listenerQueue;

	public SymbolSubstituteFactory() {
		init();
	}

	public SymbolSubstituteFactory(ApplicationData appData) {
		this();
		setApplicationData(appData);
	}

	public void init() {
		int size = definedPoolSize > 0 ? definedPoolSize : DEFAULT_POOL_SIZE;
		cbQueue = new LinkedList<ComboBoxInput>();
		tfQueue = new LinkedList<TextFieldInput>();
		labelQueue = new LinkedList<JLabel>();
		listenerQueue = new LinkedList<SymbolSubstituteListener>();
		for (int i = 0; i < size; i++) {
			cbQueue.add(new ComboBoxInput());
			tfQueue.add(new TextFieldInput());
			labelQueue.add(new JLabel());
			listenerQueue.add(new SymbolSubstituteListener());
		}
	}

	public void init(int poolSize) {
		this.definedPoolSize = poolSize;
		init();
	}

	public void setApplicationContext(ApplicationContext context) {
		ctx = context;
	}

	public ApplicationContext getApplicationContext() {
		return this.ctx;
	}

	public void setApplicationData(ApplicationData data) {
		this.appData = data;
	}

	public ApplicationData getApplicationData() {
		return this.appData;
	}

	public JComponent getSubstitute(Symbol symbol) {

		if (symbol == null) {
			return null;
		}

		SymbolType st = symbol.getSymbolType();
		if (st == SymbolType.LITERAL) {
			JLabel label = labelQueue.pollFirst();
			label.setText(((Literal) symbol).getValue());
			return label;
		} else if (st == SymbolType.VARIABLE) {
			Variable v = (Variable) symbol;
			VariableType vType = v.getType();
			SymbolSubstituteListener l = listenerQueue.pollFirst();
			l.setInputSymbol(v);
			if (vType != VariableType.UNDEFINED) {
				ComboBoxInput cbInput = cbQueue.pollFirst();
				cbInput.restrictTo(vType);
				cbInput.initElement(appData);
				cbInput.addItemListener(l);
				if (vType == VariableType.INT || vType == VariableType.FLOAT) {
					cbInput.setEditable(true);
				}

				return cbInput;
			} else {
				TextFieldInput tfInput = new TextFieldInput();
				tfInput.addActionListener(l);
				return tfInput;
			}
		}

		return null;
	}

	public void releaseSubstitute(JComponent component) {
		if (component instanceof JLabel) {
			JLabel label = (JLabel) component;
			label.setText("");
			labelQueue.add(label);
		} else if (component instanceof ComboBoxInput) {
			ComboBoxInput cbInput = (ComboBoxInput) component;
			SymbolSubstituteListener l = cbInput.getSubstituteListener();
			if (l != null) {
				l.setInputSymbol(null);
				listenerQueue.add(l);
				cbInput.setSubstituteListener(null);
			}
			cbInput.releaseElement();
			cbQueue.add(cbInput);
		} else if (component instanceof TextFieldInput) {
			TextFieldInput tfInput = (TextFieldInput) component;
			SymbolSubstituteListener l = tfInput.getSubstituteListener();
			if (l != null) {
				l.setInputSymbol(null);
				listenerQueue.add(l);
				tfInput.setSubstituteListener(null);
			}
			tfInput.releaseElement();
			tfQueue.add(tfInput);
		}
	}

	public ArrayList<JComponent> getSequenceComponents(SymbolSequence template,
			SymbolSequence translation) {
		return null;
	}

	private class ComboBoxInput extends JComboBox implements InputElement {

		private SymbolSubstituteListener listener;
		private VariableType inputRestriction;

		public ComboBoxInput() {
			super();
		}

		public ComboBoxInput(VariableType inputRestriction, ApplicationData data) {
			this();
			restrictTo(inputRestriction);
			initElement(data);
		}

		public void restrictTo(VariableType type) {
			this.inputRestriction = type;
		}

		public VariableType getRestriction() {
			return inputRestriction;
		}

		public void initElement(ApplicationData data) {
			this.setModel(data.variableData
					.getVariableListModel(inputRestriction));
		}

		public void setSubstituteListener(SymbolSubstituteListener l) {
			this.removeItemListener(listener);
			listener = l;
			if (listener != null) {
				this.addItemListener(listener);
			}
		}

		public SymbolSubstituteListener getSubstituteListener() {
			return listener;
		}

		public Object getValue() {
			System.out.println(this.getSelectedItem());
			return this.getSelectedItem();
		}

		public void setValue(Object value) {
			this.setSelectedItem(value);
		}

		public JComponent getComponent() {
			return this;
		}

		public void releaseElement() {

		}
	}

	private class TextFieldInput extends JTextField implements InputElement {

		private SymbolSubstituteListener listener;

		public TextFieldInput() {
			super();
		}

		public void initElement(ApplicationData data) {
		}

		public void setSubstituteListener(SymbolSubstituteListener l) {
			listener = l;
		}

		public SymbolSubstituteListener getSubstituteListener() {
			return listener;
		}

		public Object getValue() {
			return this.getText();
		}

		public void setValue(Object value) {
			if (value instanceof IVariable) {
				this.setText(((IVariable) value).getValue());
			} else {
				this.setText(value.toString());
			}
		}

		public void restrictTo(VariableType type) {
		}

		public VariableType getRestriction() {
			return null;
		}

		public JComponent getComponent() {
			return this;
		}

		public void releaseElement() {

		}
	}
}
